feat_schema = {
    "type": "object",
    "required": [
        "name",
        "description",
        "prerequisite_stats",
        "prerequisite_feats",
        "prerequisite_level",
    ],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "prerequisite_stats": {
            "type": "object",
            "patternProperties": {
                "^[A-Za-z]+$": {"type": "number"}
            },
            "additionalProperties": False
        },
        "prerequisite_feats": {
            "type": "array",
            "items": {"type": "string"}
        },
        "prerequisite_level": {"type": "number"},
    },
    "additionalProperties": True
}