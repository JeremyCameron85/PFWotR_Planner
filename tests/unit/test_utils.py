import pytest
from wotr_planner.models.json_loader import load_classes, load_races, load_feats

def test_load_classes_returns_list():
    """
    Test that load_classes function returns a list of classes with expected structure.
    - Verify that at least one class has a 'name' key.
    """
    classes = load_classes()
    assert isinstance(classes, list)
    assert any("name" in c for c in classes)

def test_load_races_returns_list():
    """
    Test that load_races function returns a list of races with expected structure.
    - Verify that at least one race has a 'name' key.
    """
    races = load_races()
    assert isinstance(races, list)
    assert any("name" in r for r in races)

def  test_load_feats_returns_list():
    """
    Test that load_feats function returns a list of feats with expected structure.
    - Verify that at least one feat has a 'name' key.
    """
    feats = load_feats()
    assert isinstance(feats, list)
    assert any("name" in f for f in feats)