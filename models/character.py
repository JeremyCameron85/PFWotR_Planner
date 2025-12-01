class Character:
    def __init__(self):
        self.name = ""
        self.race = None
        self.char_class = None
        self.level = 1
        self.feats = []
        self.stats = {"Str":10, "Dex":10, "Con":10, "Int":10, "Wis":10, "Cha":10}

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