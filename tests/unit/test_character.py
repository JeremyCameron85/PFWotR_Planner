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
    assert "Dodge" not in names # Dexterity prerequisite not met

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
    assert c.feats == [] # All invalid feats removed

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

def test_available_feats_append():
    c = Character()
    c.level = 5
    c.stats["Str"] = 15
    c.feats = [{"name": "Power Attack"}]

    cleave = {
        "name": "Cleave",
        "prequisite_level": 1,
        "prerequisite_stats": {"Str": 13},
        "prerequisite_feats": ["Power Attack"]
    }
    all_feats = [cleave]

    available = c.available_feats(all_feats)

    assert len(available) == 1
    assert available == [cleave]