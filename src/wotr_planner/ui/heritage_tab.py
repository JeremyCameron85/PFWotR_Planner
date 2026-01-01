from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit
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
        # Filter heritages based on race
        self.filtered_heritages = []

        # UI elements for heritage selection
        layout.addWidget(QLabel("Select Heritage:"))
        self.heritage_combo = QComboBox()
        self.heritage_combo.clear()
        layout.addWidget(self.heritage_combo)

        # Description box for heritage details
        self.description_box = QTextEdit()
        self.description_box.setReadOnly(True)
        layout.addWidget(self.description_box, stretch=1)

        # Initialize description with the first heritage
        self.update_description(self.heritage_combo.currentIndex())

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
        Update character's heritage based on selection.
        - Updates the character model and emits heritage_changed signal.
        - Updates the description box with heritage details.
        Args:
            index (int): Index of the selected heritage in the combo box.
        """
        # Validate index
        if index < 0 or index >= len(self.filtered_heritages):
            return
        
        selected_heritage = self.filtered_heritages[index]
        self.character.heritage = selected_heritage
        self.update_description(index)

        # Emit signal indicating heritage change
        self.heritage_changed.emit()

    def refresh_heritage_options(self):
        """
        Refresh the list of heritage options based on the character's race.
        - Filters heritages to match the selected race.
        - Updates the combo box with the filtered heritages.
        - Sets the character's heritage to the first available option.
        - Emits heritage_changed signal.
        """
        race_name = self.character.race["name"]
        self.filtered_heritages = [
            h for h in self.heritages if h["race"] == race_name
        ]

        # Update combo box with filtered heritages
        self.heritage_combo.blockSignals(True)
        self.heritage_combo.clear()
        self.heritage_combo.addItems([h["name"] for h in self.filtered_heritages])
        self.heritage_combo.blockSignals(False)

        # Set to first heritage if available
        if self.filtered_heritages:
            self.heritage_combo.setCurrentIndex(0)
            self.character.heritage = self.filtered_heritages[0]
            self.update_description(0)
            self.heritage_changed.emit()

    def update_description(self, index):
        """
        Update the description box with details of the selected heritage.
        Args:
            index (int): Index of the selected heritage in the combo box.
        """
        # Validate index
        if index < 0 or index >= len(self.filtered_heritages):
            self.description_box.setPlainText("")
            return
        
        heritage = self.filtered_heritages[index]
        desc = heritage.get("description", "No description available.")
        self.description_box.setPlainText(desc)
        