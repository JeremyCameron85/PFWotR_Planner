from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
import json

class BackgroundTab(QWidget):
    background_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        base_dir = Path(__file__).resolve().parent.parent
        backgrounds_path = base_dir / "data" / "backgrounds.json"
        with backgrounds_path.open(encoding="utf-8") as backgrounds_file:
            self.backgrounds = json.load(backgrounds_file)

        layout.addWidget(QLabel("Select Background:"))
        self.background_combo = QComboBox()
        self.background_combo.addItems([background["name"] for background in self.backgrounds])
        layout.addWidget(self.background_combo)

        if getattr(self.character, "background", None):
            idx = next((i for i, b in enumerate(self.backgrounds) if b["name"] == self.character.background), 0)
            self.background_combo.setCurrentIndex(idx)

        self.background_combo.currentIndexChanged.connect(self.update_background)

    def update_background(self, index):
        selected_background = self.backgrounds[index]
        self.character.background = selected_background["name"]
        self.background_changed.emit()