from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
import json

class FeatsTab(QWidget):
    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        with open("data/feats.json") as feats_file:
            self.feats = json.load(feats_file)

        layout.addWidget(QLabel("Select Feat:"))
        self.feat_combo = QComboBox()
        layout.addWidget(self.feat_combo)

        self.update_feats()

    def update_feats(self):
        self.feat_combo.clear()
        available = self.character.available_feats(self.feats)
        self.feat_combo.addItems([feat["name"] for feat in available])