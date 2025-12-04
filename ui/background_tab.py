from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
from wotr_planner.models.json_loader import load_backgrounds
import json

class BackgroundTab(QWidget):
    background_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.backgrounds = load_backgrounds()

        layout.addWidget(QLabel("Select Background:"))
        self.background_combo = QComboBox()
        self.background_combo.addItems([bg["name"] for bg in self.backgrounds])
        layout.addWidget(self.background_combo)

        if getattr(self.character, "background", None):
            idx = next(
                (i for i, b in enumerate(self.backgrounds)
                 if b["name"] == self.character.background.get("name")),
                 0
            )
            self.background_combo.setCurrentIndex(idx)

        self.background_combo.currentIndexChanged.connect(self.update_background)

    def update_background(self, index):
        selected_background = self.backgrounds[index]
        self.character.background = selected_background
        self.background_changed.emit()