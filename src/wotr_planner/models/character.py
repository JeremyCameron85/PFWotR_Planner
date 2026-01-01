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
        self.traits = []
        self.trait_bonuses = {
            "saves": {},
            "ab": {},
            "natural_attacks": [],
            "skills": {},
            "ac": 0,
            "dodge_ac": {},
            "natural_ac": 0,
            "resistances": {},
            "spell_dc": {},
            "damage_reduction": [],
            "cmb": 0,
            "cmd": 0,
            "skill_points_bonus": 0,
            "innate_abilities": [],
            "innate_feats": []
        }
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
        heritage_mod = self.trait_bonuses.get("skill_points_bonus", 0)
        return max(1, base + int_mod + race_mod + heritage_mod)
    
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
    
    def recalculate_traits(self, trait_registry):
        self.traits = []
        self.trait_bonuses = {
            "saves": {},
            "ab": {},
            "natural_attacks": [],
            "skills": {},
            "ac": 0,
            "dodge_ac": {},
            "natural_ac": 0,
            "resistances": {},
            "spell_dc": {},
            "damage_reduction": [],
            "cmb": 0,
            "cmd": 0,
            "skill_points_bonus": 0,
            "innate_abilities": [],
            "innate_feats": []
        }
        race_traits = self.race.get("traits", [])
        self.traits.extend(race_traits)

        if self.heritage and "traits_removed" in self.heritage:
            removed = set(self.heritage["traits_removed"])
            self.traits =  [t for t in self.traits if t not in removed]

        if self.heritage and "traits" in self.heritage:
            self.traits.extend(self.heritage["traits"])

        for trait_name in self.traits:
            trait_def = trait_registry.get(trait_name)
            if not trait_def:
                continue

            for save, bonus in trait_def.get("save_bonuses", {}).items():
                self.trait_bonuses["saves"][save] = \
                    self.trait_bonuses["saves"].get(save, 0) + bonus

            for creature, bonus in trait_def.get("attack_bonuses", {}).items():
                self.trait_bonuses["ab"][creature] = \
                    self.trait_bonuses["ab"].get(creature, 0) + bonus
            
            for skill, bonus in trait_def.get("skill_bonuses", {}).items():
                self.trait_bonuses["skills"][skill] = \
                    self.trait_bonuses["skills"].get(skill, 0) + bonus

            for resist, amount in trait_def.get("resistances", {}).items():
                self.trait_bonuses["resistances"][resist] = \
                    self.trait_bonuses["resistances"].get(resist, 0) + amount
            
            for school, bonus in trait_def.get("spell_dc_bonuses", {}).items():
                self.trait_bonuses["spell_dc"][school] = \
                    self.trait_bonuses["spell_dc"].get(school, 0) + bonus
                
            for creature, bonus in trait_def.get("dodge_ac_bonuses", {}).items():
                self.trait_bonuses["dodge_ac"][creature] = \
                    self.trait_bonuses["dodge_ac"].get(creature, 0) + bonus
                
            if "natural_ac_bonuses" in trait_def:
                self.trait_bonuses["natural_ac"] += trait_def["natural_ac_bonuses"]

            if "combat_maneuver_bonuses" in trait_def:
                self.trait_bonuses["cmb"] += trait_def["combat_maneuver_bonuses"]

            if "combat_maneuver_defenses" in trait_def:
                self.trait_bonuses["cmd"] += trait_def["combat_maneuver_defenses"]

            for dr in trait_def.get("damage_reduction", []):
                self.trait_bonuses["damage_reduction"].append(dr)

            for ability in trait_def.get("innate_abilities", []):
                self.trait_bonuses["innate_abilities"].append(ability)

            for feat in trait_def.get("innate_feats", []):
                self.trait_bonuses["innate_feats"].append(feat)
            
            for attack in trait_def.get("natural_attacks", []):
                self.trait_bonuses["natural_attacks"].append(attack)

        if self.heritage:
            if "skill_points_bonus" in self.heritage:
                self.trait_bonuses["skill_points_bonus"] += \
                    self.heritage["skill_points_bonus"]