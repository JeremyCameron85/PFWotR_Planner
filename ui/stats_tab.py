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
            spin.setRange(7, 18)
            spin.setValue(self.character.stats[stat])
            spin.valueChanged.connect(lambda value, s=stat: self.update_stat(s, value))
            stats_layout.addWidget(spin, row, 1)
            self.stat_widgets[stat] = spin
            row += 1

        layout.addWidget(stats_group)

    def update_stat(self, stat_name, value):
        old_value = self.character.stats[stat_name]
        self.character.stats[stat_name] = value

        if self.total_points_spent() > 25:
            self.character.stats[stat_name] = old_value
            self.stat_widgets[stat_name].setValue(old_value)
            return

        self.update_points_label()
        self.stats_changed.emit()

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
        return sum(self.point_cost(val) for val in self.character.stats.values())
    
    def update_points_label(self):
        spent = self.total_points_spent()
        remaining = 25 - spent
        self.points_label.setText(f"Points {remaining}")

    def apply_race_bonuses(self, race):
        if not race:
            return
        
        for stat, bonus in race.get("modifiers", {}).items():
            self.character.stats[stat] += bonus
            self.stat_widgets[stat].setValue(self.character.stats[stat])
        self.update_points_label()
        self.stats_changed.emit()

    def apply_heritage_modifiers(self, heritage):
        if not heritage:
            return
        for stat, bonus in heritage.get("modifiers", {}).items():
            self.character.stats[stat] += bonus
            self.stat_widgets[stat].setValue(self.character.stats[stat])
        self.update_points_label()
        self.stats_changed.emit()

    def recalculate_modifiers(self, feats):
        for feat in feats:
            for stat, bonus in feat.get("modifiers", {}).items():
                self.character.stats[stat] += bonus
                self.stat_widgets[stat].setValue(self.character.stats[stat])
            self.update_points_label()
            self.stats_changed.emit()