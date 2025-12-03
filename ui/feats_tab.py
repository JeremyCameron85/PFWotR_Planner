from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QListWidget, QPushButton
from pathlib import Path
import json

class FeatsTab(QWidget):
    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        base_dir = Path(__file__).resolve().parent.parent
        feats_path = base_dir / "data" / "feats.json"
        with feats_path.open(encoding="utf-8") as feats_file:
            self.feats = json.load(feats_file)

        layout.addWidget(QLabel("Select Feat:"))
        self.feat_combo = QComboBox()
        layout.addWidget(self.feat_combo)

        self.add_button = QPushButton("Add Feat")
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_selected_feat)

        layout.addWidget(QLabel("Selected Feats:"))
        self.selected_list = QListWidget()
        layout.addWidget(self.selected_list)

        self.update_feats()
        self.refresh_selected_feats()

    def update_feats(self):
        self.feat_combo.clear()
        available = self.character.available_feats(self.feats)
        self.feat_combo.addItems([feat["name"] for feat in available])

    def add_selected_feat(self):
        selected_feat = self.feat_combo.currentText()
        if selected_feat and selected_feat not in self.character.feats:
            self.character.feats.append(selected_feat)
            self.update_feats()
            self.refresh_selected_feats()

    def refresh_selected_feats(self):
        self.selected_list.clear()
        self.selected_list.addItems(self.character.feats)