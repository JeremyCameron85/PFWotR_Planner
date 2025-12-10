from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_skills

class SkillsTab(QWidget):
    """
    UI tab for selecting character skills.
    - Displays skill details and updates character model accordingly.
    """
    # Signal emitted when skills change
    skills_changed = pyqtSignal()

    def __init__(self, character):
        '''
        Initialize the SkillsTab UI.
        - Loads skills from JSON.
        - Sets up UI elements for skill selection.
        '''
        # Initialize parent QWidget
        super().__init__()
        self.character = character       
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Skill points display
        self.points_label = QLabel()
        layout.addWidget(self.points_label)
        # Update skill points display
        self.update_skill_points()
        self.skills = load_skills()

        # Skills group box and layout
        skills_group = QGroupBox("Skills")
        skills_layout = QGridLayout()
        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)

        # Skill widgets and effective skill labels
        self.skill_widgets = {}
        self.effective_labels = {}

        # List of skills
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

        # Populate skills layout
        row = 0
        for skill in skills:
            # Add label and spin box for each skill
            skills_layout.addWidget(QLabel(skill), row, 0)
            spin = QSpinBox()
            # Set spin box range and initial value
            spin.setRange(0, self.character.level)
            spin.setValue(self.character.skill_ranks.get(skill, 0))
            # Connect signal for skill value change
            spin.valueChanged.connect(lambda value, s=skill: self.update_skill(s, value))
            # Add spin box and effective skill label to layout
            skills_layout.addWidget(spin, row, 1)
            self.skill_widgets[skill] = spin
            effective_label = QLabel(str(self.character.skills.get(skill, 0)))
            skills_layout.addWidget(effective_label, row, 2)
            self.effective_labels[skill] = effective_label
            # Increment row for next skill
            row += 1

        # Add skills group to main layout
        layout.addWidget(skills_group)

    def update_skill(self, skill_name, new_value):
        """
        Update character skill rank based on user input.
        - Validates against available skill points and character level.
        Args:
            skill_name (str): Name of the skill being updated.
            new_value (int): New value for the skill rank.
        """
        # Get old skill rank value
        old_value = self.character.skill_ranks.get(skill_name, 0)
        # Calculate change in skill points
        delta = new_value - old_value
        # Validate against available skill points
        if delta > self.skill_points_pool():
            spin = self.skill_widgets[skill_name]
            # Revert to old value if not enough points
            spin.blockSignals(True)
            spin.setValue(old_value)
            spin.blockSignals(False)
            return
        
        # Validate against character level
        if new_value > self.character.level:
            spin = self.skill_widgets[skill_name]
            # Revert to max level if exceeded
            spin.blockSignals(True)
            spin.setValue(self.character.level)
            spin.blockSignals(False)
            # Emit skills changed signal
            self.skills_changed.emit()
            return
        
        # Update character skill rank
        self.character.skill_ranks[skill_name] = new_value
        # Recalculate effective skills and update UI
        self.recalculate_effective_skills()
        self.update_skill_points()
        # Emit skills changed signal
        self.skills_changed.emit()
    
    def update_skill_points(self):
        """
        Update the display of available skill points.
         - Calculates remaining skill points based on character level and spent points.
        """
        points = self.skill_points_pool()
        # Update label with remaining skill points
        self.points_label.setText(f"Skill Points {points}")

    def skill_points_pool(self):
        """
        Calculate remaining skill points available for allocation.
        Returns:
            int: Remaining skill points.
        """
        # Calculate remaining skill points
        return self.character.level * self.character.skill_points_per_level() - sum(self.character.skill_ranks.values())

    def recalculate_effective_skills(self):
        """
        Recalculate effective skill values based on ranks, feats, and background.
        - Updates the character's effective skills and UI labels accordingly.
        """
        # Reset effective skills to current ranks
        self.character.skills = self.character.skill_ranks.copy()
        # Apply feat modifiers
        for feat in self.character.feats:
            for skill, bonus in feat.get("skill_modifiers", {}).items():
                # Update effective skill value
                self.character.skills[skill] = self.character.skills.get(skill, 0) + bonus

        # Apply background skill modifiers
        if self.character.background:
            for skill, bonus in self.character.background.get("skill_modifiers", {}).items():
                # Update effective skill value
                self.character.skills[skill] = self.character.skills.get(skill, 0) + bonus

        # Update UI labels for effective skills
        for skill, label in self.effective_labels.items():
            label.setText(str(self.character.skills.get(skill, 0)))

    def apply_level_up(self, new_level):
        """
        Apply level up to character and update skill UI accordingly.
        - Sets character level to new level.
        Args:
            new_level (int): New level of the character.
        """
        self.character.level = new_level
        # Update skill spin box ranges
        for skill, spin in self.skill_widgets.items():
            spin.setRange(0, self.character.level)
        # Recalculate effective skills and update skill points
        self.update_skill_points()

    def enforce_skill_point_limit(self):
        """
        Enforce skill point allocation limit based on character level.
         - Reduces skill ranks if they exceed available skill points.
        """
        # Calculate allowed and spent skill points
        allowed = self.character.level * self.character.skill_points_per_level()
        spent = sum(self.character.skill_ranks.values())
        # No adjustment needed if within limit
        if spent <= allowed:
            return
        
        # Reduce skill ranks starting from lowest priority skills
        skills_sorted = list(reversed(self.skill_widgets.keys()))

        # Iterate through skills and reduce ranks as needed
        for skill in skills_sorted:
            while spent > allowed and self.character.skill_ranks[skill] > 0:
                self.character.skill_ranks[skill] -= 1
                spent -= 1

        # Update UI spin boxes to reflect adjusted skill ranks
        for skill, spin in self.skill_widgets.items():
            spin.blockSignals(True)
            spin.setValue(self.character.skill_ranks[skill])
            spin.blockSignals(False)

        # Recalculate effective skills and update skill points
        self.recalculate_effective_skills()
        self.update_skill_points()