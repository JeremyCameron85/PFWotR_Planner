from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
import json

class FeatsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        with open("data/feats.json") as feats_file:
            self.feats = json.load(feats_file)

        layout.addWidget(QLabel("Select Feat:"))
        self.feat_combo = QComboBox()
        self.feat_combo.addItems([feat["name"] for feat in self.feats])
        layout.addWidget(self.feat_combo)