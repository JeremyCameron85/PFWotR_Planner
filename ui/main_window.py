from PyQt6.QtWidgets import QMainWindow, QTabWidget
from ui.character_tab import CharacterTab
from ui.skills_tab import SkillsTab
from ui.feats_tab import FeatsTab
from models.character import Character

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PFWotR Character Planner")
        self.resize(800, 600)

        self.character = Character()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.character_tab = CharacterTab(self.character)
        self.skills_tab = SkillsTab(self.character)
        self.feats_tab = FeatsTab(self.character)

        self.character_tab.stats_changed.connect(self.feats_tab.update_feats)

        self.tabs.addTab(self.character_tab, "Character")
        self.tabs.addTab(self.skills_tab, "Skills")
        self.tabs.addTab(self.feats_tab, "Feats")