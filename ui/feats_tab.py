from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QListWidget, QPushButton
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
from wotr_planner.models.json_loader import load_feats
import json

class FeatsTab(QWidget):
    feats_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.feats = load_feats()

        layout.addWidget(QLabel("Select Feat:"))
        self.feat_combo = QComboBox()
        layout.addWidget(self.feat_combo)

        self.add_button = QPushButton("Add Feat")
        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_selected_feat)

        layout.addWidget(QLabel("Selected Feats:"))
        self.selected_list = QListWidget()
        layout.addWidget(self.selected_list)

        self.remove_button = QPushButton("Remove Feat")
        layout.addWidget(self.remove_button)
        self.remove_button.clicked.connect(self.remove_selected_feat)

        self.update_feats()
        self.refresh_selected_feats()

    def update_feats(self):
        self.feat_combo.clear()
        available = self.character.available_feats(self.feats)
        
        if available:
            self.feat_combo.addItems([f["name"] for f in available])
        else:
            self.feat_combo.addItem("No feats available placeholder text")

    def add_selected_feat(self):
        selected_feat = self.feat_combo.currentText()
        chosen_feat = next((f for f in self.feats if f["name"] == selected_feat), None)
        if not chosen_feat:
            return
        
        for prereq in chosen_feat.get("prerequisite_feats", []):
            if prereq not in [f["name"] for f in self.character.feats]:
                return
            
        for stat, value in chosen_feat.get("prerequisite_stats", {}).items():
            if self.character.stats.get(stat, 0) < value:
                return
            
        if self.character.level < chosen_feat.get("prerequisite_level", 1):
            return
        
        if chosen_feat["name"] not in [f["name"] for f in self.character.feats]:
            self.character.feats.append(chosen_feat)
            self.update_feats()
            self.refresh_selected_feats()
            self.feats_changed.emit()

    def remove_selected_feat(self):
        selected_items = self.selected_list.selectedItems()
        if not selected_items:
            return
        
        feat_name = selected_items[0].text()
        self.character.feats = [f for f in self.character.feats if f["name"] != feat_name]
        removed = {feat_name}
        changed = True
        while changed:
            changed = False
            for feat in list(self.character.feats):
                prereqs = feat.get("prerequisite_feats",  [])
                if any(req  in removed for req in prereqs):
                    self.character.feats.remove(feat)
                    removed.add(feat["name"])
                    changed = True
                    
        self.update_feats()
        self.refresh_selected_feats()
        self.feats_changed.emit()

    def refresh_selected_feats(self):
        self.selected_list.clear()
        self.selected_list.addItems([f["name"] for f in self.character.feats])