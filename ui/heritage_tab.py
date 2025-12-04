from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
from wotr_planner.models.json_loader import load_heritages
import json

class HeritageTab(QWidget):
    heritage_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.heritages = load_heritages()

        layout.addWidget(QLabel("Select Heritage:"))
        self.heritage_combo = QComboBox()
        self.heritage_combo.addItems([heritage["name"] for heritage in self.heritages])
        layout.addWidget(self.heritage_combo)

        if getattr(self.character, "heritage", None):
            idx = next(
                (i for i, h in enumerate(self.heritages)
                 if h["name"] == self.character.heritage),
                 0
            )
            self.heritage_combo.setCurrentIndex(idx)

        self.heritage_combo.currentIndexChanged.connect(self.update_heritage)

    def update_heritage(self, index):
        selected_heritage = self.heritages[index]
        self.character.heritage = selected_heritage
        self.heritage_changed.emit()