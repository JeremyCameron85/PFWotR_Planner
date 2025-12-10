from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QTextEdit
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_classes

class ClassTab(QWidget):
    """
    UI tab for selecting character class and archetype.
    - Displays class and archetype details and updates character model accordingly.
    """
    # Signal emitted when class or archetype changes
    class_changed = pyqtSignal()

    def __init__(self, character):
        """
        Initialize the ClassTab UI.
        - Loads classes from JSON.
        - Sets up UI elements for class and archetype selection.
        """
        # Initialize parent QWidget
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Load classes from JSON
        self.classes = load_classes()

        # UI elements for class selection
        layout.addWidget(QLabel("Select Class:"))
        self.class_tree = QTreeWidget()
        self.class_tree.setHeaderHidden(True)
        layout.addWidget(self.class_tree)

        # Description box for class/archetype details
        self.description_box = QTextEdit()
        self.description_box.setReadOnly(True)
        layout.addWidget(self.description_box, stretch=1)

        # Populate class tree
        self.populate_classes()
        # Connect signal for item selection
        self.class_tree.itemClicked.connect(self.on_item_selected)

    def populate_classes(self):
        """
        Populate the class tree with classes and their archetypes.
        - Each class is a parent item.
        - Each archetype is a child item under its class.
        """
        self.class_tree.clear()
        for cls in self.classes:
            # Create parent item for class
            parent_item = QTreeWidgetItem([cls["name"]])
            parent_item.setData(0, 1, cls) # Store class data
            self.class_tree.addTopLevelItem(parent_item)

            # Add archetypes as child items
            for arch in cls.get("archetypes", []):
                child_item = QTreeWidgetItem([arch["name"]])
                child_item.setData(0, 1, arch) # Store archetype data
                parent_item.addChild(child_item)

        # Collapse all items initially
        self.class_tree.collapseAll()

    def on_item_selected(self, item, column):
        """
        Handle selection of class or archetype from the tree.
        - If a class is selected, set character's class and clear archetype.
        - If an archetype is selected, set character's class and archetype.
        - Update description box with relevant information.
        - Emit signal indicating change.
        Args:
            item (QTreeWidgetItem): The selected item.
            column (int): The column index (Always 0 in this single-column tree).
        """
        parent = item.parent()
        if parent is None:
            # Selected item is a class
            self.class_tree.collapseAll()
            item.setExpanded(True)
            cls = item.data(0, 1) # Get class data
            self.character.char_class = cls
            self.character.archetype = None
            self.description_box.setPlainText(cls.get("description", "No description available."))
        else:
            # Selected item is an archetype
            arch = item.data(0, 1) # Get archetype data
            base_cls = parent.data(0, 1) # Get parent class data
            self.character.char_class = base_cls
            self.character.archetype = arch["name"]
            self.description_box.setPlainText(arch.get("description", "No description available."))

        # Emit signal indicating class/archetype change
        self.class_changed.emit()