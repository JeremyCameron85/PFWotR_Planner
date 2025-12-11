import pytest
from PyQt6.QtWidgets import QTreeWidgetItem
from wotr_planner.ui.classes_tab import ClassTab
from wotr_planner.models.character import Character

@pytest.fixture
def dummy_classes(monkeypatch):
    """
    Fixture to provide dummy class data for testing.
    Args:
        monkeypatch: pytest fixture to modify behavior for testing.
    """
    test_data = [
        {
            "name": "Fighter",
            "description": "A brave warrior skilled in combat.",
            "archetypes": [
                {"name": "Armiger", "description": "A master of arms."}
            ]
        }
    ]
    # Override the load_classes function to return test data
    monkeypatch.setattr("wotr_planner.ui.classes_tab.load_classes", lambda: test_data)
    return test_data

def test_initialization(qtbot, dummy_classes):
    """
    Test that the ClassTab initializes correctly with dummy class data.
    Args:
        qtbot: pytest-qt fixture for testing Qt widgets.
        dummy_classes: fixture providing dummy class data.
    """
    char = Character(char_class={}, race={})
    tab = ClassTab(char)
    qtbot.addWidget(tab)

    assert tab.class_tree is not None
    assert tab.description_box.isReadOnly()

    assert tab.classes == dummy_classes
    assert tab.class_tree.topLevelItemCount() == 1 # One class

def test_select_class_updates_character(qtbot, dummy_classes):
    """
    Test that selecting a class updates the character and description box.
    Args:
        qtbot: pytest-qt fixture for testing Qt widgets.
        dummy_classes: fixture providing dummy class data.
    """
    char = Character(char_class={}, race={})
    tab = ClassTab(char)
    qtbot.addWidget(tab)

    fighter_item = tab.class_tree.topLevelItem(0)

    with qtbot.waitSignal(tab.class_changed):
        tab.on_item_selected(fighter_item, 0)

    assert char.char_class["name"] == "Fighter"
    assert char.archetype is None
    assert "brave" in tab.description_box.toPlainText()

def test_select_archetype_updates_character(qtbot, dummy_classes):
    """
    Test that selecting an archetype updates the character and description box.
    Args:
        qtbot: pytest-qt fixture for testing Qt widgets.
        dummy_classes: fixture providing dummy class data.
    """
    char = Character(char_class={}, race={})
    tab = ClassTab(char)
    qtbot.addWidget(tab)

    fighter_item = tab.class_tree.topLevelItem(0)
    archetype_item = fighter_item.child(0)

    with qtbot.waitSignal(tab.class_changed):
        tab.on_item_selected(archetype_item, 0)

    assert char.char_class["name"] == "Fighter"
    assert char.archetype ==  "Armiger"
    assert "master" in tab.description_box.toPlainText()

def test_select_class_without_description(qtbot, monkeypatch):
    """
    Test selecting a class without a description.
    Args:
        qtbot: pytest-qt fixture for testing Qt widgets.
        monkeypatch: pytest fixture to modify behavior for testing.
    """
    test_data = [
        {
            "name": "Unknown Class",
            "archetypes": []
        }
    ]
    # Override the load_classes function to return test data
    monkeypatch.setattr("wotr_planner.ui.classes_tab.load_classes", lambda: test_data)

    char = Character(char_class={}, race={})
    tab = ClassTab(char)
    qtbot.addWidget(tab)

    unkown_item = tab.class_tree.topLevelItem(0)

    with qtbot.waitSignal(tab.class_changed):
        tab.on_item_selected(unkown_item, 0)

    assert char.char_class["name"] == "Unknown Class"
    assert char.archetype is None
    assert tab.description_box.toPlainText() == "No description available."