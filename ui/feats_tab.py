from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QListWidget, QPushButton
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
import json

class FeatsTab(QWidget):
    feats_changed = pyqtSignal()

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
        
        if available:
            self.feat_combo.addItems([feat["name"] for feat in available])
        else:
            self.feat_combo.addItem("No feats available placeholder text")

    def add_selected_feat(self):
        selected_feat = self.feat_combo.currentText()
        chosen_feat = next((feat for feat in self.feats if feat["name"] == selected_feat), None)
        if chosen_feat and chosen_feat["name"] not in [feat["name"] for feat in self.character.feats]:
            self.character.feats.append(chosen_feat)
            self.update_feats()
            self.refresh_selected_feats()
            self.feats_changed.emit()

    def refresh_selected_feats(self):
        self.selected_list.clear()
        self.selected_list.addItems([feat["name"] for feat in self.character.feats])