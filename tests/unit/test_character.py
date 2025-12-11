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