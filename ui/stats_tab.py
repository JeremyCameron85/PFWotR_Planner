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
            spin.setRange(1, 20)
            spin.setValue(self.character.stats[stat])
            spin.valueChanged.connect(lambda value, s=stat: self.update_stat(s, value))
            stats_layout.addWidget(spin, row, 1)
            self.stat_widgets[stat] = spin
            row += 1

        layout.addWidget(stats_group)

    def update_stat(self, stat_name, value):
        self.character.stats[stat_name] = value
        self.stats_changed.emit()