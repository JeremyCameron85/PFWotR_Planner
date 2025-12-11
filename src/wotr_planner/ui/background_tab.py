from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_backgrounds

class BackgroundTab(QWidget):
    """
    UI tab for selecting character background.
    - Displays background details and updates character model accordingly.
    """
    # Signal emitted when background changes
    background_changed = pyqtSignal()

    def __init__(self, character):
        """
        Initialize the BackgroundTab UI.
        - Loads backgrounds from JSON.
        - Sets up UI elements for background selection.
        """
        # Initialize parent QWidget
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Load backgrounds from JSON
        self.backgrounds = load_backgrounds()

        # UI elements for background selection
        layout.addWidget(QLabel("Select Background:"))
        self.background_combo = QComboBox()
        self.background_combo.addItems([bg["name"] for bg in self.backgrounds])
        layout.addWidget(self.background_combo)

        # Set current background if already selected
        if getattr(self.character, "background", None):
            idx = next(
                (i for i, b in enumerate(self.backgrounds)
                 if b["name"] == self.character.background.get("name")),
                 0 # Default to first background if not found
            )
            self.background_combo.setCurrentIndex(idx)

        # Connect signal for background change
        self.background_combo.currentIndexChanged.connect(self.update_background)

    def update_background(self, index):
        """
        Update character background based on selection.
        - Sets the character's background to the selected one.
        - Emits a signal indicating the background has changed.
        Args:
            index (int): Index of the selected background in the combo box.
        """
        selected_background = self.backgrounds[index]
        self.character.background = selected_background
        # Emit signal indicating background change
        self.background_changed.emit()