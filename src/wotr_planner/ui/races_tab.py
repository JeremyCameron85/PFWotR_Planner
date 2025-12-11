from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_races

class RaceTab(QWidget):
    """
    UI tab for selecting character race.
    - Displays race details and updates character model accordingly.
    """
    # Signal emitted when race changes
    race_changed = pyqtSignal()

    def __init__(self, character):
        """
        Initialize the RaceTab UI.
        - Loads races from JSON.
        - Sets up UI elements for race selection.
        """
        # Initialize parent QWidget
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Load races from JSON
        self.races = load_races()

        # UI elements for race selection
        layout.addWidget(QLabel("Select Race:"))
        self.race_combo = QComboBox()
        self.race_combo.addItems([race["name"] for race in self.races])     
        layout.addWidget(self.race_combo)

        # Set current race if already selected
        if getattr(self.character, "race", None):
            idx = next(
                (i for i, r in enumerate(self.races)
                 if r["name"] == self.character.race.get("name")),
                 0 # Default to first race if not found
            )
            self.race_combo.setCurrentIndex(idx)
       
        # Connect signal for race change
        self.race_combo.currentIndexChanged.connect(self.update_race)

    def update_race(self, index):
        """
        Update character race based on selection.
        - Sets the character's race to the selected one.
        - Emits a signal indicating the race has changed.
        Args:
            index (int): Index of the selected race in the combo box.
        """
        selected_race = self.races[index]
        self.character.race = selected_race
        # Emit signal indicating race change
        self.race_changed.emit()