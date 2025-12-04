from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
import json

class StatsTab(QWidget):
    stats_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        stats_group = QGroupBox("Ability Scores")
        stats_layout = QGridLayout()
        stats_group.setLayout(stats_layout)
        self.stat_widgets = {}

        self.points_label = QLabel()
        layout.addWidget(self.points_label)
        self.update_points_label()

        stats = [
            "Str",
            "Dex",
            "Con",
            "Int",
            "Wis",
            "Cha"
        ]

        row = 0
        for stat in stats:
            stats_layout.addWidget(QLabel(stat), row, 0)
            spin = QSpinBox()
            racial_mod = self.character.race.get("modifiers", {}).get(stat, 0) if self.character.race  else 0
            spin.setRange(7 + racial_mod, 18 + racial_mod)
            spin.setValue(self.character.point_buy_stats[stat] + racial_mod)
            spin.valueChanged.connect(lambda value, s=stat: self.update_stat(s, value))
            stats_layout.addWidget(spin, row, 1)
            self.stat_widgets[stat] = spin
            row += 1

        layout.addWidget(stats_group)

    def update_stat(self, stat_name, displayed_value):
        racial_mod = 0
        if self.character.heritage:
            racial_mod = self.character.heritage.get("modifiers", {}).get(stat_name, 0)
        elif self.character.race:
            racial_mod = self.character.race.get("modifiers", {}).get(stat_name, 0)
        else:
            racial_mod = 0
        
        base_value = displayed_value - racial_mod
        old_value = self.character.point_buy_stats[stat_name]
        self.character.point_buy_stats[stat_name] = base_value

        if self.total_points_spent() > 25:
            self.character.point_buy_stats[stat_name] = old_value
            spin = self.stat_widgets[stat_name]
            spin.blockSignals(True)
            spin.setValue(old_value + racial_mod)
            spin.blockSignals(False)
            return

        self.recalculate_modifiers(self.character.feats)

    @staticmethod
    def point_cost(value: int) -> int:
        if value < 10:
            if value == 9:
                return -1
            elif value == 8:
                return -2
            elif value == 7:
                return -4

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

        return 0
    
    def total_points_spent(self) -> int:
        return sum(self.point_cost(val) for val in self.character.point_buy_stats.values())
    
    def update_points_label(self):
        spent = self.total_points_spent()
        remaining = 25 - spent
        self.points_label.setText(f"Points {remaining}")

    def apply_race_bonuses(self, race):
        self.character.race = race
        self.recalculate_modifiers(self.character.feats)

    def apply_heritage_modifiers(self, heritage):
        self.character.heritage = heritage
        self.recalculate_modifiers(self.character.feats)

    def recalculate_modifiers(self, feats):
        self.character.stats = self.character.point_buy_stats.copy()
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
        
        for stat, spin in self.stat_widgets.items():
            if self.character.heritage:
                racial_mod = self.character.heritage.get("modifiers", {}).get(stat, 0)
            elif self.character.race:
                racial_mod = self.character.race.get("modifiers", {}).get(stat, 0)
            else:
                racial_mod = 0

            spin.blockSignals(True)
            spin.setRange(7 + racial_mod, 18 + racial_mod)
            spin.setValue(self.character.point_buy_stats[stat] + racial_mod)
            spin.blockSignals(False)

        self.update_points_label()
        self.stats_changed.emit()