import pytest
import json
import importlib.resources as resources
from jsonschema import validate

# Define the JSON schema for races
RACE_SCHEMA = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string"},
        "bonus_feats": {"type":  "array", "items": {"type": "integer"}},
        "skill_points_bonus": {"type": "integer"}
    }
}

def test_race_json_schema():
    """
    Test that all races in races.json conform to the RACE_SCHEMA.
    - Load races.json
    - Validates each race against the RACE_SCHEMA.
    """
    with resources.files("wotr_planner.data").joinpath("races.json").open("r") as f:
        data = json.load(f)
    for race in data:
        validate(instance=race, schema=RACE_SCHEMA)