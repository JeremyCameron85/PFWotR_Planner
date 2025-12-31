import json
from jsonschema import validate
from wotr_planner.models.json_loader import load_feats
from wotr_planner.models.feat_schema import feat_schema

def test_feats_json_schema():
    feats = load_feats()
    for feat in feats:
        validate(instance=feat, schema=feat_schema)