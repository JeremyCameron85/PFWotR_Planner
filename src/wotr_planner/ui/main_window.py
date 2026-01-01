from PyQt6.QtWidgets import QMainWindow, QTabWidget
from wotr_planner.ui.classes_tab import ClassTab
from wotr_planner.ui.races_tab import RaceTab
from wotr_planner.ui.stats_tab import StatsTab
from wotr_planner.ui.skills_tab import SkillsTab
from wotr_planner.ui.feats_tab import FeatsTab
from wotr_planner.ui.background_tab import BackgroundTab
from wotr_planner.ui.heritage_tab import HeritageTab
from wotr_planner.models.character import Character

class MainWindow(QMainWindow):
    """
    Main application window containing all character planner tabs.
    - Initializes character model and connects tab signals for updates.
    - Manages overall character data and interactions between tabs.
    """
    def __init__(self):
        """
        Initialize the MainWindow UI.
        - Sets up tabs for class, race, heritage, background, stats, skills, and feats.
        - Connects signals to handle updates across tabs.
        """
        # Initialize parent QMainWindow
        super().__init__()
        self.setWindowTitle("PFWotR Character Planner")
        self.resize(800, 600)

        # Initialize character model
        self.character = Character()

        # Set up tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize tabs
        self.classes_tab = ClassTab(self.character)
        self.races_tab = RaceTab(self.character)
        self.heritage_tab = HeritageTab(self.character)
        self.heritage_tab.refresh_heritage_options()
        self.background_tab = BackgroundTab(self.character)
        self.stats_tab = StatsTab(self.character)
        self.skills_tab = SkillsTab(self.character)
        self.feats_tab = FeatsTab(self.character)

        # Connect signals for inter-tab updates
        self.classes_tab.class_changed.connect(self.on_class_changed)
        self.races_tab.race_changed.connect(self.on_race_changed)
        self.background_tab.background_changed.connect(self.on_background_changed)
        self.heritage_tab.heritage_changed.connect(self.on_heritage_changed)
        self.stats_tab.stats_changed.connect(self.on_stats_changed)
        self.feats_tab.feats_changed.connect(self.on_feats_changed)

        # Add tabs to the tab widget
        self.tabs.addTab(self.classes_tab, "Class")
        self.tabs.addTab(self.races_tab, "Race")
        self.tabs.addTab(self.heritage_tab, "Heritage")
        self.tabs.addTab(self.background_tab, "Background")
        self.tabs.addTab(self.stats_tab, "Ability Scores")
        self.tabs.addTab(self.skills_tab, "Skills")
        self.tabs.addTab(self.feats_tab, "Feats")

    def on_race_changed(self):
        """
        Update character and UI when race changes.
        - Applies race bonuses and updates related tabs.
        - Recalculates skills based on new race.
        - Updates skill points display.
        """
        self.stats_tab.apply_race_bonuses(self.character.race)
        self.heritage_tab.refresh_heritage_options()
        self.character.validate_feats(self.feats_tab.feats)
        self.feats_tab.update_feats()
        self.feats_tab.refresh_selected_feats()
        self.skills_tab.recalculate_effective_skills()
        self.skills_tab.enforce_skill_point_limit()
        self.skills_tab.update_skill_points()

    def on_class_changed(self):
        """
        Update character and UI when class changes.
        - Validates feats and updates related tabs.
        - Recalculates skills based on new class.
        - Updates skill points display.
        """
        self.character.validate_feats(self.feats_tab.feats)
        self.feats_tab.update_feats()
        self.feats_tab.refresh_selected_feats()         
        self.skills_tab.recalculate_effective_skills()
        self.skills_tab.enforce_skill_point_limit()
        self.skills_tab.update_skill_points()

    def on_feats_changed(self):
        """
        Update character and UI when feats change.
        - Recalculates stats and skills based on selected feats.
        - Updates skill points display.
        """
        self.stats_tab.recalculate_modifiers(self.character.feats)
        self.skills_tab.recalculate_effective_skills()
        self.skills_tab.enforce_skill_point_limit()
        self.skills_tab.update_skill_points()

    def on_background_changed(self):
        """
        Update character and UI when background changes.
        - Recalculates skills based on new background.
        - Updates skill points display.
        """
        self.feats_tab.update_feats()
        self.skills_tab.recalculate_effective_skills()
        self.skills_tab.enforce_skill_point_limit()
        self.skills_tab.update_skill_points()

    def on_heritage_changed(self):
        """
        Update character and UI when heritage changes.
        - Applies heritage modifiers and updates related tabs.
        - Recalculates skills based on new heritage.
        - Updates skill points display.
        """
        self.stats_tab.apply_heritage_modifiers(self.character.heritage)
        self.character.validate_feats(self.feats_tab.feats)
        self.feats_tab.update_feats()
        self.feats_tab.refresh_selected_feats()
        self.skills_tab.recalculate_effective_skills()
        self.skills_tab.enforce_skill_point_limit()
        self.skills_tab.update_skill_points()

    def on_stats_changed(self):
        """
        Update character and UI when stats change.
        - Validates feats and updates related tabs.
        - Recalculates skills based on new stats.
        - Updates skill points display.
        """
        self.character.validate_feats(self.feats_tab.feats)
        self.feats_tab.update_feats()
        self.feats_tab.refresh_selected_feats()
        self.skills_tab.recalculate_effective_skills()
        self.skills_tab.enforce_skill_point_limit()
        self.skills_tab.update_skill_points()