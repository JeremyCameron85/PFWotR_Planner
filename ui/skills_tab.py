from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
import json

class SkillsTab(QWidget):
    skills_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        base_dir = Path(__file__).resolve().parent.parent
        skills_path = base_dir / "data" / "skills.json"
        with skills_path.open(encoding="utf-8") as skills_file:
            self.skills = json.load(skills_file)

        skills_group = QGroupBox("Skills")
        skills_layout = QGridLayout()
        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)

        self.skill_widgets = {}

        skills = [
            "Athletics",
            "Mobility",
            "Trickery",
            "Stealth",
            "Knowledge(Arcana)",
            "Knowledge(World)",
            "Lore(Nature)",
            "Lore(Religion)",
            "Perception",
            "Persuasion",
            "Use Magic Device"
        ]

        row = 0
        for skill in skills:
            skills_layout.addWidget(QLabel(skill), row, 0)
            spin = QSpinBox()
            spin.setRange(0, 20)
            spin.setValue(self.character.skills.get(skill, 0))
            spin.valueChanged.connect(lambda value, s=skill: self.update_skill(s, value))
            skills_layout.addWidget(spin, row, 1)
            self.skill_widgets[skill] = spin
            row += 1

        layout.addWidget(skills_group)

    def update_skill(self, skill_name, value):
        self.character.skills[skill_name] = value
        self.skills_changed.emit()