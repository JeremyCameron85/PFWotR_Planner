from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
from wotr_planner.models.json_loader import load_classes
import json

class ClassTab(QWidget):
    class_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.classes = load_classes()

        layout.addWidget(QLabel("Select Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItems([char_class["name"] for char_class in self.classes])
        layout.addWidget(self.class_combo)

        if getattr(self.character, "char_class", None):
            idx = next(
                (i for i, c in enumerate(self.classes)
                 if c["name"] == self.character.char_class.get("name")),
                 0
            )
            self.class_combo.setCurrentIndex(idx)

        self.class_combo.currentIndexChanged.connect(self.update_class)

    def update_class(self, index):
        selected_class = self.classes[index]
        self.character.char_class = selected_class
        self.class_changed.emit()