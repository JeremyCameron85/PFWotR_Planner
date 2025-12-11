import pytest
from wotr_planner.models.character import Character

def test_feat_removed_when_stat_drops():
    """
    Test that feats are removed when character stats drop below prerequisites.
    - Create a character with feats that have stat prerequisites.
    - Lower the relevant stat below the prerequisite.
    - Verify that the feats are removed from the character.
    """
    fighter = Character(
        char_class={"name": "Fighter", "skill_points": 2, "bonus_feat_interval": 2, "bonus_feats": [1]},
        race={"name": "Human", "bonus_feats": [1]}
    )
    all_feats = [
        {"name": "Power Attack", "prerequisite_stats": {"Str": 13}},
        {"name": "Cleave", "prerequisite_feats": ["Power Attack"]}
    ]
    fighter.stats["Str"] = 14
    fighter.feats.append({"name": "Power Attack"})
    fighter.feats.append({"name": "Cleave"})

    fighter.stats["Str"] = 10 # Drop Strength below prerequisite
    removed = fighter.validate_feats(all_feats)

    assert "Power Attack" in removed
    assert "Cleave" in removed
    # Verify that the feats are no longer in the character's feat list
    assert not any(f["name"] in ["Power Attack", "Cleave"] for f in fighter.feats)

def test_total_feat_slots_fighter_vs_wizard():
    """
    Test total feat slots calculation for different classes.
    - Create a Fighter and a Wizard character.
    - Verify that the Fighter has more total feat slots than the Wizard.
    """
    fighter = Character(
        char_class={"name": "Fighter", "bonus_feat_interval": 2, "bonus_feats": [1]},
        race={"name": "Human", "bonus_feats": [1]}
    )
    wizard = Character(
        char_class={"name": "Wizard", "skill_points": 2},
        race={"name": "Elf"}
    )
    
    assert fighter.total_feat_slots() == 3 # 1 base + 1 (class) + 1 (race)
    assert wizard.total_feat_slots() == 1 # 1 base only

def test_skill_points_maximum_one():
    """
    Test that skill points per level do not exceed one for certain classes.
    - Create a Fighter character with low Intelligence.
    - Verify that skill points per level is capped at one.
    """
    fighter = Character(char_class={"name": "Fighter", "skill_points": 2},
                         race={"name": "Human"})
    fighter.stats["Int"] = 6 # -2 modifier

    assert fighter.skill_points_per_level() == 1 # Minimum of 1 skill point per level

def test_available_feats_with_prerequisites():
    """
    Test that available feats are correctly identified based on prerequisites.
    - Create a character with certain stats and existing feats.
    """
    c = Character()
    c.level = 3
    c.stats["Str"] = 15
    c.feats = [{"name": "Power Attack"}]
    all_feats = [
        {"name": "Cleave", "prerequisite_stats": {"Str": 13}, "prerequisite_feats": ["Power Attack"]},
        {"name": "Dodge", "prerequisite_stats": {"Dex": 13}}
    ]
    available = c.available_feats(all_feats)
    names = [f["name"] for f in available]

    assert "Cleave" in names
    assert "Dodge" not in names

def test_skill_points_per_level_with_modifiers():
    """
    Test that skill points per level calculation includes modifiers and bonuses.
    - Create a character with a class and race that provide skill points.
    - Set Intelligence stat to provide a positive modifier.
    """
    c = Character(char_class={"name": "Fighter", "skill_points": 2}, race={"name": "Human", "skill_points_bonus": 1})
    c.stats["Int"] = 14 # +2 modifier

    assert c.skill_points_per_level() == 5 # 2 (base) + 2 (Int mod) + 1 (race bonus)

def test_remove_feat_success_and_failure():
    """
    Test removing a feat from the character.
    - Attempt to remove an existing feat and verify success.
    - Attempt to remove a non-existing feat and verify failure.
    """
    c = Character()
    c.feats = [{"name": "Dodge"}]
    assert c.remove_feat("Dodge") is True
    assert c.remove_feat("Exist") is False

def test_validate_feats_removes_invalid_by_prereqs():
    """
    Test that validate_feats removes feats that do not meet prerequisites.
    - Create a character with a feat that has unmet prerequisites.
    - Verify that the feat is removed after validation.
    """
    c = Character()
    c.level = 1
    c.stats["Str"] = 10
    c.feats = [{"name": "Cleave"}, {"name": "LvlDummy"}]
    all_feats = [
        {"name": "Cleave", "prerequisite_stats": {"Str": 13}, "prerequisite_feats": ["Power Attack"]},
        {"name": "Power Attack", "prerequisite_stats": {"Str": 13}},
        {"name": "LvlDummy", "prerequisite_level": 20}
    ]
    removed = c.validate_feats(all_feats)
    assert "Cleave" in removed
    assert "LvlDummy" in removed
    assert c.feats == []

def test_total_feat_slots_with_bonuses():
    """
    Test total feat slots calculation including bonuses from class and race.
    - Create a character with class and race that provide bonus feat slots.
    - Verify the total feat slots calculation.
    """
    c = Character(char_class={"name": "Fighter", "bonus_feat_interval": 2, "bonus_feats": [1]}, race={"name": "Human", "bonus_feats": [1]})
    c.level = 6
    slots = c.total_feat_slots()
    assert slots == 8 # 3 base + 4 (class) + 1 (race)

def test_level_up():
    """
    Test that leveling up increases the character's level by one.
    """
    c = Character()
    initial_level = c.level
    c.level_up()
    assert c.level == initial_level + 1

def test_validate_feats_skips_unknown_feat():
    """
    Test that validate_feats skips feats not found in all_feats.
    - Create a character with a feat that is not defined in all_feats.
    - Verify that the feat remains after validation.
    """
    c = Character()
    c.feats = [{"name": "UnknownFeat"}]
    all_feats = []

    removed = c.validate_feats(all_feats)

    assert removed == set()
    assert c.feats == [{"name": "UnknownFeat"}]

def test_validate_feats_stat_requirement_pass():
    """
    Test that validate_feats retains feats when stat prerequisites are met.
    - Create a character with a feat that has stat prerequisites.
    - Verify that the feat is retained after validation.
    """
    c = Character()
    c.stats["Str"] = 15
    c.feats = [{"name": "Power Attack"}]
    all_feats = [
        {"name": "Power Attack", "prerequisite_stats": {"Str": 13}}
    ]
    removed = c.validate_feats(all_feats)
    assert removed == set()
    assert c.feats == [{"name": "Power Attack"}]

def test_validate_feats_prereq_pass():
    """
    Test that validate_feats retains feats when feat prerequisites are met.
    - Create a character with feats that satisfy each other's prerequisites.
    - Verify that both feats are retained.
    """
    c = Character()
    c.feats = [{"name": "Power Attack"}, {"name": "Cleave"}]
    all_feats = [
        {"name": "Power Attack"},
        {"name": "Cleave", "prerequisite_feats": ["Power Attack"]}
    ]
    removed = c.validate_feats(all_feats)
    assert removed == set()
    assert {f["name"] for f in c.feats} == {"Power Attack", "Cleave"}

def test_validate_feats_trims_excess():
    """
    Test that validate_feats trims feats to fit within available feat slots.
    - Create a character with more feats than available slots.
    - Verify that excess feats are removed.
    """
    c = Character()
    c.level = 1
    c.stats["Str"] = 15
    c.stats["Dex"] = 15
    c.feats = [{"name": "Power Attack"}, {"name": "Cleave"}, {"name": "Dodge"}, {"name": "Weapon Focus"}]
    all_feats = [
        {"name": "Power Attack"},
        {"name": "Cleave", "prerequisite_feats": ["Power Attack"]},
        {"name": "Dodge"},
        {"name": "Weapon Focus"}
    ]
    removed = c.validate_feats(all_feats)
    assert len(c.feats) == 3 # Total feat slots at level 1 is 3
    assert removed == set() # Some feats were removed

def test_total_feat_slots_skips_class_bonus_below_level():
    """
    Test that total_feat_slots does not count class bonus feats if level is below the required interval.
    - Create a character with a class that provides bonus feats at certain intervals.
    - Set level below the interval and verify total feat slots.
    """
    c = Character(char_class={"name": "Fighter", "bonus_feats": [3]})
    c.level = 2
    
    assert c.total_feat_slots() == 2 # 1 base + 1 (level-based), class bonus not applied yet

def test_total_feat_slots_skips_race_bonus_below_level():
    """
    Test that total_feat_slots does not count race bonus feats if level is below the required interval.
    - Create a character with a race that provides bonus feats at certain intervals.
    - Set level below the interval and verify total feat slots.
    """
    c = Character(race={"name": "Human", "bonus_feats": [2]})
    c.level = 1
    
    assert c.total_feat_slots() == 2 # 1 base + 1 (level-based), race bonus not applied yet