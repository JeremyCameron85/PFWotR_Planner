import pytest
import json
import importlib.resources as resources
from jsonschema import validate

# Define the JSON schema for a feat
FEAT_SCHEMA = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "prerequisite_level": {"type": "integer"},
        "prerequisite_stats": {"type": "object"},
        "prerequisite_feats": {"type": "array", "items": {"type": "string"}},
        "modifiers": {"type": "object"}
    }
}

def test_feat_json_schema():
    """
    Test that all feats in feats.json conform to the FEAT_SCHEMA.
    - Loads feats.json
    - Validates each feat against the FEAT_SCHEMA.
    """
    with resources.files("wotr_planner.data").joinpath("feats.json").open("r") as f:
        data = json.load(f)
    for feat in data:
        validate(instance=feat, schema=FEAT_SCHEMA)