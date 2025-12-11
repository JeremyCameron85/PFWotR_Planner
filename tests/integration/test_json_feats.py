import pytest
from wotr_planner.models.json_loader import load_feats

def test_power_attack_has_strength_prereq():
    """
    Test that the Power Attack feat has the correct Strength prerequisite in the JSON data.
    - prerequisite_stats with Str >= 13
    """
    feats = load_feats()
    pa = next(f for f in feats if f["name"] == "Power Attack")
    assert "prerequisite_stats" in pa
    assert pa["prerequisite_stats"]["Str"] >= 13 # Ensure Strength prerequisite is at least 13