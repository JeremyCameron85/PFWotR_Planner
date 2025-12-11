from wotr_planner.models.json_loader import load_classes, load_races

class Character:
    """
    Character model representing a player character.
    Stores class, race, stats, skills, feats, and other attributes.
    Provides methods to manage and validate character data.
    """
    def __init__(self, char_class=None, race=None):
        """
        Initialize a Character instance.
        Args:
            char_class (dict, optional): Character class data. Defaults to None.
            race (dict, optional): Character race data. Defaults to None.
        """
        # Loads json definitions
        classes = load_classes()
        races = load_races()
        self.name = ""
        # Default to Human Fighter if none provided
        self.race = race or next(r for r in races if r["name"] == "Human")
        self.char_class = char_class or next(c for c in classes if c["name"] == "Fighter")
        self.heritage = None
        self.background = None
        self.level = 1
        self.feats = []
        # Initialize stats
        self.point_buy_stats = {
            "Str":10,
            "Dex":10, 
            "Con":10, 
            "Int":10, 
            "Wis":10, 
            "Cha":10
        }
        # Copy of base stats for reference
        self.base_stats = self.point_buy_stats.copy()
        # Current stats including racial/heritage modifiers
        self.stats = self.point_buy_stats.copy()

        # Initialize skills
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
        # Current effective skills including modifiers
        self.skills = self.skill_ranks.copy()

    def level_up(self):
        """
        Increase character level by 1.
        """
        self.level += 1
    
    def available_feats(self, all_feats):
        """
        Get list of feats available for selection based on current character state.
        - Considers level, stats, and already selected feats.
        Args:
            all_feats: List of all possible feat definitions.
        Returns:
            List of available feat definitions.
        """
        feats_list = []
        chosen_feat_names = [f["name"] for f in self.feats]
        for feat in all_feats:
            # Level requirement
            feat_level = feat.get("prerequisite_level", 1) <= self.level
            # Stat requirements
            feat_stats = all(
                self.stats.get(stat, 0) >= val
                for stat, val in feat.get("prerequisite_stats", {}).items()
            )
            # Feat prerequisites
            required_feats = feat.get("prerequisite_feats", [])
            feat_feats = all(req in chosen_feat_names for req in required_feats)

            if feat_level and feat_stats and feat_feats:
                feats_list.append(feat)
                print("APPEND HIT")

        return feats_list
    
    def skill_points_per_level(self) -> int:
        """
        Calculate skill points gained per level based on class, race, and intelligence.
        Returns:
            int: Number of skill points gained per level.
        """
        base = self.char_class.get("skill_points", 0)
        int_mod = (self.stats["Int"] - 10) // 2
        race_mod = self.race.get("skill_points_bonus", 0)
        return max(1, base + int_mod + race_mod)
    
    def remove_feat(self, feat_name: str):
        """
        Remove a feat from the character by name.
        Args:
            feat_name (str): Name of the feat to remove.
        Returns:
            bool: True if a feat was removed, False otherwise.
        """
        before =  len(self.feats)
        self.feats = [f for f in self.feats if f["name"] != feat_name]
        return len(self.feats) < before
    
    def validate_feats(self, all_feats):
        """
        Validate current feats against prerequisites and slot limits.
        - Removes feats that no longer meet prerequisites.
        - Trim feats to fit within available feat slots.
        Args:
            all_feats: List of all possible feat definitions.
        Returns:
            set: Names of removed feats.
        """
        removed = set()
        changed = True
        while changed:
            changed = False
            for feat in list(self.feats):
                full_def = next((f  for f in all_feats if f["name"] == feat["name"]), None)
                if not full_def:
                    continue

                # Check level prerequisite
                if self.level < full_def.get("prerequisite_level", 1):
                    self.feats = [f for f in self.feats if f["name"] != feat["name"]]
                    removed.add(feat["name"])
                    changed = True
                    continue

                # Check stat prerequisites
                for stat, value in full_def.get("prerequisite_stats", {}).items():
                    if self.stats.get(stat, 0) < value:
                        self.feats = [f for f in self.feats if f["name"] != feat["name"]]
                        removed.add(feat["name"])
                        changed = True
                        break

                # Check feat prerequisites
                for prereq in full_def.get("prerequisite_feats", []):
                    if prereq not in [f["name"] for f in self.feats]:
                        self.feats = [f for f in self.feats if f["name"] != feat["name"]]
                        removed.add(feat["name"])
                        changed = True
                        break

        # Enforce maximum feat slots
        max_slots = self.total_feat_slots()
        if len(self.feats) > max_slots:
            self.feats = self.feats[:max_slots]
            removed.update(f["name"] for f in self.feats[max_slots:])

        return removed

    def total_feat_slots(self) -> int:
        """
        Calculate total feat slots available based on level, class, and race.
        Returns:
            int: Total number of feat slots available.
        """
        slots = 0
        # Feats every odd level
        slots += (self.level + 1) // 2
        # Class bonus feats
        bonus_interval = self.char_class.get("bonus_feat_interval")
        if bonus_interval:
            slots += self.level // bonus_interval

        # Additional class bonus feats
        for lvl in self.char_class.get("bonus_feats", []):
            if self.level >= lvl:
                slots += 1
        
        # Race bonus feats
        for lvl in self.race.get("bonus_feats", []):
            if self.level >= lvl:
                slots += 1
        return slots