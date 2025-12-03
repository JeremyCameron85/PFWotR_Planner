from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
import json

class RaceTab(QWidget):
    race_changed = pyqtSignal()

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

        if getattr(self.character, "race", None):
            idx = next((i for i, r in enumerate(self.races) if r["name"] == self.character.race), 0)
            self.race_combo.setCurrentIndex(idx)

        self.race_combo.currentIndexChanged.connect(self.update_race)

    def update_race(self, index):
        selected_race = self.races[index]
        self.character.race = selected_race["name"]
        self.race_changed.emit()