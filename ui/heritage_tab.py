from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_heritages

class HeritageTab(QWidget):
    """
    UI tab for selecting character heritage.
    - Displays heritage details and updates character model accordingly.
    """
    # Signal emitted when heritage changes
    heritage_changed = pyqtSignal()

    def __init__(self, character):
        """
        Initialize the HeritageTab UI.
        - Loads heritages from JSON.
        - Sets up UI elements for heritage selection.
        """
        # Initialize parent QWidget
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Load heritages from JSON
        self.heritages = load_heritages()

        # UI elements for heritage selection
        layout.addWidget(QLabel("Select Heritage:"))
        self.heritage_combo = QComboBox()
        self.heritage_combo.addItems([heritage["name"] for heritage in self.heritages])
        layout.addWidget(self.heritage_combo)

        # Set current heritage if already selected
        if getattr(self.character, "heritage", None):
            idx = next(
                (i for i, h in enumerate(self.heritages)
                 if h["name"] == self.character.heritage),
                 0 # Default to first heritage if not found
            )
            self.heritage_combo.setCurrentIndex(idx)

        # Connect signal for heritage change
        self.heritage_combo.currentIndexChanged.connect(self.update_heritage)

    def update_heritage(self, index):
        """
        Update character heritage based on selection.
        - Sets the character's heritage to the selected one.
        - Emits a signal indicating the heritage has changed.
        Args:
            index (int): Index of the selected heritage in the combo box.
        """
        selected_heritage = self.heritages[index]
        self.character.heritage = selected_heritage
        # Emit signal indicating heritage change
        self.heritage_changed.emit()