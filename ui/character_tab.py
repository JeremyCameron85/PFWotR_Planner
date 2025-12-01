from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
import json
class CharacterTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        with open("data/races.json") as races_file:
            self.races = json.load(races_file)

        layout.addWidget(QLabel("Select Race:"))
        self.race_combo = QComboBox()
        self.race_combo.addItems([race["name"] for race in self.races])
        layout.addWidget(self.race_combo)

        with open("data/classes.json") as classes_file:
            self.classes = json.load(classes_file)

        layout.addWidget(QLabel("Select Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItems([char_class["name"] for char_class in self.classes])
        layout.addWidget(self.class_combo)