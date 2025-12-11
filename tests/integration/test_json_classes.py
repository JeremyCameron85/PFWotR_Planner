import pytest
from wotr_planner.models.json_loader import load_classes

def test_fighter_class_has_expected_fields():
    """
    Test that the Fighter class has the expected fields in the JSON data.
    - base_hp
    - skill_points
    - bonus_feats
    """
    classes = load_classes()
    fighter =  next(c for c in classes if c["name"] == "Fighter")
    assert "base_hp" in fighter
    assert "skill_points" in fighter
    assert "bonus_feats" in fighter