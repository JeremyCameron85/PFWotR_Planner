from wotr_planner.models.json_loader import load_classes, load_races

class Character:
    def __init__(self, char_class=None, race=None):
        classes = load_classes()
        races = load_races()
        self.name = ""
        self.race = race or next(r for r in races if r["name"] == "Human")
        self.char_class = char_class or next(c for c in classes if c["name"] == "Fighter")
        self.heritage = None
        self.background = None
        self.level = 1
        self.feats = []
        self.point_buy_stats = {
            "Str":10,
            "Dex":10, 
            "Con":10, 
            "Int":10, 
            "Wis":10, 
            "Cha":10
        }
        self.base_stats = self.point_buy_stats.copy()
        self.stats = self.point_buy_stats.copy()

        self.skill_ranks = {
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
        self.skills = self.skill_ranks.copy()

    def level_up(self):
        self.level += 1
    
    def available_feats(self, all_feats):
        feats_list = []
        chosen_feat_names = [f["name"] for f in self.feats]
        for feat in all_feats:
            feat_level = feat.get("prerequisite_level", 1) <= self.level
            feat_stats = all(
                self.stats.get(stat, 0) >= val
                for stat, val in feat.get("prerequisite_stats", {}).items()
            )
            required_feats = feat.get("prerequisite_feats", [])
            feat_feats = all(req in chosen_feat_names for req in required_feats)

            if feat_level and feat_stats and feat_feats:
                feats_list.append(feat)

        return feats_list
    
    def skill_points_per_level(self) -> int:
        base = self.char_class.get("skill_points", 0)
        int_mod = (self.stats["Int"] - 10) // 2
        race_mod = self.race.get("skill_points_bonus", 0)
        return max(1, base + int_mod + race_mod)
    
    def remove_feat(self, feat_name: str):
        before =  len(self.feats)
        self.feats = [f for f in self.feats if f["name"] != feat_name]
        return len(self.feats) < before
    
    def validate_feats(self, all_feats):
        removed = set()
        changed = True
        while changed:
            changed = False
            for feat in list(self.feats):
                full_def = next((f  for f in all_feats if f["name"] == feat["name"]), None)
                if not full_def:
                    continue

                if self.level < full_def.get("prerequisite_level", 1):
                    self.feats = [f for f in self.feats if f["name"] != feat["name"]]
                    removed.add(feat["name"])
                    changed = True
                    continue

                for stat, value in full_def.get("prerequisite_stats", {}).items():
                    if self.stats.get(stat, 0) < value:
                        self.feats = [f for f in self.feats if f["name"] != feat["name"]]
                        removed.add(feat["name"])
                        changed = True
                        break

                for prereq in full_def.get("prerequisite_feats", []):
                    if prereq not in [f["name"] for f in self.feats]:
                        self.feats = [f for f in self.feats if f["name"] != feat["name"]]
                        removed.add(feat["name"])
                        changed = True
                        break

    def total_feat_slots(self) -> int:
        slots = 0
        slots += 1
        slots += (self.level - 1) // 3
        bonus_interval = self.char_class.get("bonus_feat_interval")
        if bonus_interval:
            slots += self.level // bonus_interval
        
        for lvl in self.race.get("bonus_feats", []):
            if self.level >= lvl:
                slots += 1
        return slots