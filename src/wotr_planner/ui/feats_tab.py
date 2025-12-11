from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QListWidget, QPushButton, QTextEdit
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_feats

class FeatsTab(QWidget):
    """
    UI tab for selecting character feats.
    - Displays feat details and updates character model accordingly.
    """
    # Signal emitted when feats change
    feats_changed = pyqtSignal()

    def __init__(self, character):
        """
        Initialize the FeatsTab UI.
        - Loads feats from JSON.
        - Sets up UI elements for feat selection and management.
        """
        # Initialize parent QWidget
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Load feats from JSON
        self.feats = load_feats()

        # UI elements for feat selection and management
        layout.addWidget(QLabel("Select Feat:"))
        self.feat_combo = QComboBox()
        layout.addWidget(self.feat_combo)
        self.feat_combo.currentIndexChanged.connect(self.show_feat_description)

        # Description box for feat details
        self.description_box = QTextEdit()
        self.description_box.setReadOnly(True)
        layout.addWidget(self.description_box, stretch=1)

        # Button to add selected feat
        self.add_button = QPushButton("Add Feat")
        layout.addWidget(self.add_button)
        # Connect signal for adding selected feat
        self.add_button.clicked.connect(self.add_selected_feat)

        # List of selected feats
        layout.addWidget(QLabel("Selected Feats:"))
        self.selected_list = QListWidget()
        layout.addWidget(self.selected_list)
        # Connect signal for selected feat description display
        self.selected_list.itemClicked.connect(self.show_selected_feat_description)

        # Button to remove selected feat
        self.remove_button = QPushButton("Remove Feat")
        layout.addWidget(self.remove_button)
        # Connect signal for removing selected feat
        self.remove_button.clicked.connect(self.remove_selected_feat)

        # Initialize feat list and selected feats display
        self.update_feats()
        self.refresh_selected_feats()

    def show_feat_description(self):
        """
        Display description of the currently selected feat in the combo box.
         - Updates the description box with the feat's details.
        """
        selected_feat = self.feat_combo.currentText()
        feat = next((f for f in self.feats if f["name"] == selected_feat), None)
        if feat:
            # Update description box with feat details
            self.description_box.setPlainText(feat.get("description", "No description available."))

    def show_selected_feat_description(self, item):
        """
        Display description of the selected feat from the selected feats list.
         - Updates the description box with the feat's details.
        Args:
            item (QListWidgetItem): The selected item from the list.
        """
        feat_name = item.text()
        feat = next((f for f in self.feats if f["name"] == feat_name), None)
        if feat:
            # Update description box with feat details
            self.description_box.setPlainText(feat.get("description", "No description available."))

    def update_feats(self):
        """
        Update the available feats in the combo box based on character state.
         - Considers level, stats, and already selected feats.
        """
        self.feat_combo.clear()
        available = self.character.available_feats(self.feats)
        
        if available:
            # Populate combo box with available feats
            self.feat_combo.addItems([f["name"] for f in available])
        else:
            # No available feats
            self.feat_combo.addItem("No feats available placeholder text")

    def add_selected_feat(self):
        """
        Add the currently selected feat from the combo box to the character.
         - Validates prerequisites before adding.
         - Updates the selected feats display and emits change signal.
        """
        selected_feat = self.feat_combo.currentText()
        chosen_feat = next((f for f in self.feats if f["name"] == selected_feat), None)
        # Invalid feat selected
        if not chosen_feat:
            return
        
        # No available feat slots
        if len(self.character.feats) >= self.character.total_feat_slots():
            return

        # Check prerequisites
        for prereq in chosen_feat.get("prerequisite_feats", []):
            # Prerequisite feat not met
            if prereq not in [f["name"] for f in self.character.feats]:
                return
        
        # Check stat prerequisites
        for stat, value in chosen_feat.get("prerequisite_stats", {}).items():
            # Stat prerequisite not met
            if self.character.stats.get(stat, 0) < value:
                return
        
        # Check level prerequisite
        if self.character.level < chosen_feat.get("prerequisite_level", 1):
            return
        
        # Add feat if not already selected
        if chosen_feat["name"] not in [f["name"] for f in self.character.feats]:
            self.character.feats.append(chosen_feat)
            # Update UI and emit change signal
            self.update_feats()
            self.refresh_selected_feats()
            self.feats_changed.emit()

    def remove_selected_feat(self):
        """
        Remove the currently selected feat from the selected feats list.
         - Updates the selected feats display and emits change signal.
        """
        selected_items = self.selected_list.selectedItems()
        # No feat selected
        if not selected_items:
            return
        
        feat_name = selected_items[0].text()
        # Remove feat from character
        self.character.remove_feat(feat_name)
        # Update UI and emit change signal
        self.update_feats()
        self.refresh_selected_feats()
        self.feats_changed.emit()

    def refresh_selected_feats(self):
        """
        Refresh the display of selected feats in the list widget.
         - Clears and repopulates the list with current character feats.
        """
        self.selected_list.clear()
        # Populate list with selected feats
        self.selected_list.addItems([f["name"] for f in self.character.feats])