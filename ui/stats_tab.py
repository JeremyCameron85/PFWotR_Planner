from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
import json

class CharacterTab(QWidget):
    stats_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        base_dir = Path(__file__).resolve().parent.parent
        races_path = base_dir / "data" / "races.json"
        with races_path.open(encoding="utf-8") as races_file:
            self.races = json.load(races_file)

        layout.addWidget(QLabel("Select Race:"))
        self.race_combo = QComboBox()
        self.race_combo.addItems([race["name"] for race in self.races])
        layout.addWidget(self.race_combo)

        classes_path = base_dir / "data" / "classes.json"
        with classes_path.open(encoding="utf-8") as classes_file:
            self.classes = json.load(classes_file)

        layout.addWidget(QLabel("Select Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItems([char_class["name"] for char_class in self.classes])
        layout.addWidget(self.class_combo)

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