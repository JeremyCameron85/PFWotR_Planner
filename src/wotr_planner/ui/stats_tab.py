from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal

class StatsTab(QWidget):
    """
    UI tab for selecting character ability scores.
    - Displays ability score details and updates character model accordingly.
    """
    # Signal emitted when stats change
    stats_changed = pyqtSignal()

    def __init__(self, character):
        """
        Initialize the StatsTab UI.
        - Sets up UI elements for ability score selection.
        """
        # Initialize parent QWidget
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Ability scores group box and layout
        stats_group = QGroupBox("Ability Scores")
        stats_layout = QGridLayout()
        stats_group.setLayout(stats_layout)
        self.stat_widgets = {}

        # Points label
        self.points_label = QLabel()
        layout.addWidget(self.points_label)
        # Update points label
        self.update_points_label()

        # Ability scores
        stats = [
            "Str",
            "Dex",
            "Con",
            "Int",
            "Wis",
            "Cha"
        ]

        # Populate stats layout
        row = 0
        for stat in stats:
            # Add label and spin box for each ability score
            stats_layout.addWidget(QLabel(stat), row, 0)
            spin = QSpinBox()
            # Set spin box range and initial value considering racial modifiers
            racial_mod = self.character.race.get("modifiers", {}).get(stat, 0) if self.character.race  else 0
            spin.setRange(7 + racial_mod, 18 + racial_mod)
            spin.setValue(self.character.point_buy_stats[stat] + racial_mod)
            # Connect signal for stat value change
            spin.valueChanged.connect(lambda value, s=stat: self.update_stat(s, value))
            # Add spin box to layout
            stats_layout.addWidget(spin, row, 1)
            self.stat_widgets[stat] = spin
            # Increment row for next stat
            row += 1

        # Add stats group to main layout
        layout.addWidget(stats_group)

    def update_stat(self, stat_name, displayed_value):
        """
        Update character ability score based on selection.
        - Sets the character's ability score to the selected one.
        - Ensures total points spent do not exceed 25.
        - Emits a signal indicating the stats have changed.
        Args:
            stat_name (str): Name of the ability score being updated.
            displayed_value (int): The displayed value of the ability score including racial modifiers.
        """
        # Determine racial/heritage modifier
        racial_mod = 0
        if self.character.heritage:
            racial_mod = self.character.heritage.get("modifiers", {}).get(stat_name, 0)
        elif self.character.race:
            racial_mod = self.character.race.get("modifiers", {}).get(stat_name, 0)
        else:
            racial_mod = 0
        
        # Calculate base value without racial modifiers
        base_value = displayed_value - racial_mod
        # Store old value in case we need to revert
        old_value = self.character.point_buy_stats[stat_name]
        # Update character's point buy stats
        self.character.point_buy_stats[stat_name] = base_value

        # Check if total points spent exceed 25
        if self.total_points_spent() > 25:
            # Revert to old value if exceeded
            self.character.point_buy_stats[stat_name] = old_value
            # Revert spin box to old value with racial modifiers
            spin = self.stat_widgets[stat_name]
            spin.blockSignals(True)
            spin.setValue(old_value + racial_mod)
            spin.blockSignals(False)
            return

        # Recalculate modifiers and update UI
        self.recalculate_modifiers(self.character.feats)

    @staticmethod
    def point_cost(value: int) -> int:
        """
        Calculate the point cost for a given ability score value.
        Args:
            value (int): Ability score value.
        Returns:
            int: Point cost associated with the ability score value.
        """
        # Costs for scores below 10
        if value < 10:
            if value == 9:
                return -1
            elif value == 8:
                return -2
            elif value == 7:
                return -4

        # Costs for scores 11 and above
        if value == 11:
            return 1
        elif value == 12:
            return 2
        elif value == 13:
            return 3
        elif value == 14:
            return 5
        elif value == 15:
            return 7
        elif value == 16:
            return 10
        elif value == 17:
            return 13
        elif value == 18:
            return 17

        # Default cost
        return 0
    
    def total_points_spent(self) -> int:
        """
        Calculate the total points spent on ability scores.
        Returns:
            int: Total points spent.
        """
        return sum(self.point_cost(val) for val in self.character.point_buy_stats.values())
    
    def update_points_label(self):
        """
        Update the points label to show remaining points.
        """
        spent = self.total_points_spent()
        remaining = 25 - spent
        self.points_label.setText(f"Points {remaining}")

    def apply_race_bonuses(self, race):
        """
        Apply race bonuses to character and recalculate stats
        Args:
            race (dict): Race information containing modifiers.
        """
        self.character.race = race
        self.recalculate_modifiers(self.character.feats)

    def apply_heritage_modifiers(self, heritage):
        """
        Apply heritage modifiers to character and recalculate stats.
        - Updates character heritage and recalculates modifiers.
        Args:
            heritage (dict): Heritage information containing modifiers.
        """
        self.character.heritage = heritage
        self.recalculate_modifiers(self.character.feats)

    def recalculate_modifiers(self, feats):
        """
        Recalculate character ability scores based on point buy, race, heritage, and feats.
        - Updates the character's ability scores and UI elements accordingly.
        Args:
            feats (list): List of character feats affecting ability scores.
        """
        # Reset stats to point buy values
        self.character.stats = self.character.point_buy_stats.copy()
        # Apply race, heritage, and feat modifiers
        if self.character.race:
            for stat, bonus in self.character.race.get("modifiers", {}).items():
                self.character.stats[stat] += bonus

        if self.character.heritage:
            for stat, bonus in self.character.heritage.get("modifiers", {}).items():
                race_bonus = self.character.race.get("modifiers", {}).get(stat, 0) if self.character.race else 0
                self.character.stats[stat] -= race_bonus
                self.character.stats[stat] += bonus

        for feat in feats:
            for stat, bonus in feat.get("modifiers", {}).items():
                self.character.stats[stat] += bonus
        
        # Update spin boxes to reflect current stats with racial/heritage modifiers
        for stat, spin in self.stat_widgets.items():
            if self.character.heritage:
                racial_mod = self.character.heritage.get("modifiers", {}).get(stat, 0)
            elif self.character.race:
                racial_mod = self.character.race.get("modifiers", {}).get(stat, 0)
            else:
                racial_mod = 0

            # Update spin box value
            spin.blockSignals(True)
            # Set the range and value of the spin box based on racial modifiers
            spin.setRange(7 + racial_mod, 18 + racial_mod)
            # Set value to current stat plus racial modifier
            spin.setValue(self.character.point_buy_stats[stat] + racial_mod)
            spin.blockSignals(False)

        # Update points label and emit stats changed signal
        self.update_points_label()
        self.stats_changed.emit()