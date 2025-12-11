import pytest
import json
import importlib.resources as resources
from jsonschema import validate

# Define the expected schema for class definitions
CLASS_SCHEMA = {
    "type": "object",
    "required": ["name", "base_hp", "skill_points"],
    "properties": {
        "name": {"type": "string"},
        "base_hp": {"type": "integer", "minimum": 1},
        "skill_points": {"type": "integer", "minimum": 0},
        "bonus_feats": {"type":  "array", "items": {"type": "integer"}}
    }
}

def test_class_schema():
    """
    Test that all class definitions in classes.json conform to the CLASS_SCHEMA.
    - Loads classes.json
    - Validates each class definition against the CLASS_SCHEMA
    """
    with resources.files("wotr_planner.data").joinpath("classes.json").open("r") as f:
        data = json.load(f)
    for cls in data:
        validate(instance=cls, schema=CLASS_SCHEMA)