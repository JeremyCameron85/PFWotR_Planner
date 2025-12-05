from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_skills

class SkillsTab(QWidget):
    skills_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character       
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.points_label = QLabel()
        layout.addWidget(self.points_label)
        self.update_skill_points()
        self.skills = load_skills()
        skills_group = QGroupBox("Skills")
        skills_layout = QGridLayout()
        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)
        self.skill_widgets = {}
        self.effective_labels = {}

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
            spin.setRange(0, self.character.level)
            spin.setValue(self.character.skill_ranks.get(skill, 0))
            spin.valueChanged.connect(lambda value, s=skill: self.update_skill(s, value))
            skills_layout.addWidget(spin, row, 1)
            self.skill_widgets[skill] = spin
            effective_label = QLabel(str(self.character.skills.get(skill, 0)))
            skills_layout.addWidget(effective_label, row, 2)
            self.effective_labels[skill] = effective_label
            row += 1

        layout.addWidget(skills_group)

    def update_skill(self, skill_name, new_value):
        old_value = self.character.skill_ranks.get(skill_name, 0)
        delta = new_value - old_value
        if delta > self.skill_points_pool():
            spin = self.skill_widgets[skill_name]
            spin.blockSignals(True)
            spin.setValue(old_value)
            spin.blockSignals(False)
            return
        
        if new_value > self.character.level:
            spin = self.skill_widgets[skill_name]
            spin.blockSignals(True)
            spin.setValue(self.character.level)
            spin.blockSignals(False)
            self.skills_changed.emit()
            return
        
        self.character.skill_ranks[skill_name] = new_value
        self.recalculate_effective_skills()
        self.update_skill_points()
        self.skills_changed.emit()
    
    def update_skill_points(self):
        points = self.skill_points_pool()
        self.points_label.setText(f"Skill Points {points}")

    def skill_points_pool(self):
        return self.character.level * self.character.skill_points_per_level() - sum(self.character.skill_ranks.values())

    def recalculate_effective_skills(self):
        self.character.skills = self.character.skill_ranks.copy()
        for feat in self.character.feats:
            for skill, bonus in feat.get("skill_modifiers", {}).items():
                self.character.skills[skill] = self.character.skills.get(skill, 0) + bonus

        if self.character.background:
            for skill, bonus in self.character.background.get("skill_modifiers", {}).items():
                self.character.skills[skill] = self.character.skills.get(skill, 0) + bonus

        for skill, label in self.effective_labels.items():
            label.setText(str(self.character.skills.get(skill, 0)))

    def apply_level_up(self, new_level):
        self.character.level = new_level
        for skill, spin in self.skill_widgets.items():
            spin.setRange(0, self.character.level)
        self.update_skill_points()

    def enforce_skill_point_limit(self):
        allowed = self.character.level * self.character.skill_points_per_level()
        spent = sum(self.character.skill_ranks.values())
        if spent <= allowed:
            return
        
        skills_sorted = list(reversed(self.skill_widgets.keys()))

        for skill in skills_sorted:
            while spent > allowed and self.character.skill_ranks[skill] > 0:
                self.character.skill_ranks[skill] -= 1
                spent -= 1

        for skill, spin in self.skill_widgets.items():
            spin.blockSignals(True)
            spin.setValue(self.character.skill_ranks[skill])
            spin.blockSignals(False)

        self.recalculate_effective_skills()
        self.update_skill_points()