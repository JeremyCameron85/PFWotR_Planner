from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QTextEdit
from PyQt6.QtCore import pyqtSignal
from wotr_planner.models.json_loader import load_classes

class ClassTab(QWidget):
    class_changed = pyqtSignal()

    def __init__(self, character):
        super().__init__()
        self.character = character
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.classes = load_classes()

        layout.addWidget(QLabel("Select Class:"))
        self.class_tree = QTreeWidget()
        self.class_tree.setHeaderHidden(True)
        layout.addWidget(self.class_tree)

        self.description_box = QTextEdit()
        self.description_box.setReadOnly(True)
        layout.addWidget(self.description_box, stretch=1)

        self.populate_classes()
        self.class_tree.itemClicked.connect(self.on_item_selected)

    def populate_classes(self):
        self.class_tree.clear()
        for cls in self.classes:
            parent_item = QTreeWidgetItem([cls["name"]])
            parent_item.setData(0, 1, cls)
            self.class_tree.addTopLevelItem(parent_item)

            for arch in cls.get("archetypes", []):
                child_item = QTreeWidgetItem([arch["name"]])
                child_item.setData(0, 1, arch)
                parent_item.addChild(child_item)

        self.class_tree.collapseAll()

    def on_item_selected(self, item, column):
        parent = item.parent()
        if parent is None:
            self.class_tree.collapseAll()
            item.setExpanded(True)
            cls = item.data(0, 1)
            self.character.char_class = cls
            self.character.archetype = None
            self.description_box.setPlainText(
                f"{cls['name']} (Hit Die: d{cls['hit_die']}, Skill Points: {cls['skill_points']})"
            )
        else:
            arch = item.data(0, 1)
            base_cls = parent.data(0, 1)
            self.character.char_class = base_cls
            self.character.archetype = arch["name"]
            self.description_box.setPlainText(arch.get("description", "No description available."))

        self.class_changed.emit()