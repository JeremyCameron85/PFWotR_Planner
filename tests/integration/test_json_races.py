import pytest
from wotr_planner.models.json_loader import load_races

def test_human_race_has_bonus_feat():
    """
    Test that the Human race has the expected bonus feat in the JSON data.
    - bonus_feats includes 1 bonus feat
    """
    races = load_races()
    human = next(r for r in races if r["name"] == "Human")
    assert "bonus_feats" in human
    assert 1 in human["bonus_feats"]  # Humans should have 1 bonus feat