class Character:
    def __init__(self):
        self.name = ""
        self.race = None
        self.char_class = None
        self.level = 1
        self.feats = []
        self.stats = {
            "Str":10,
            "Dex":10, 
            "Con":10, 
            "Int":10, 
            "Wis":10, 
            "Cha":10
        }
        self.skills = {
            "Athletics": 0,
            "Mobility": 0,
            "Trickery": 0,
            "Stealth": 0,
            "Knowledge(Arcana)": 0,
            "Knowledge(World)": 0,
            "Lore(Nature)": 0,
            "Lore(Religion)": 0,
            "Perception": 0,
            "Persuasion": 0,
            "Use Magic Device": 0
        }

    def level_up(self):
        self.level += 1

    def available_feats(self, all_feats):
        feats_list = []
        for feat in all_feats:
            feat_level = feat.get("prerequisite_level", 1) <= self.level
            feat_stats = all(
                self.stats.get(stat,0) >= val
                for stat, val in feat.get("prerequisite_stats", {}).items()
            )
            required_feats = feat.get("prerequisite_feats", [])
            feat_feats = all(req in self.feats for req in required_feats)

            if feat_level and feat_stats and feat_feats:
                feats_list.append(feat)
        return feats_list