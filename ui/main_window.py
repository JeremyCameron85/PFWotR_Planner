from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from ui.character_tab import CharacterTab
from ui.feats_tab import FeatsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PFWotR Character Planner")
        self.resize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.character_tab = CharacterTab()
        self.feats_tab = FeatsTab()

        self.tabs.addTab(self.character_tab, "Character")
        self.tabs.addTab(self.feats_tab, "Feats")