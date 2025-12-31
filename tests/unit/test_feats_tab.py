import pytest
from PyQt6.QtCore import Qt
from jsonschema import validate
from wotr_planner.models.character import Character
from wotr_planner.models.feat_schema import feat_schema
from wotr_planner.ui.feats_tab import FeatsTab

@pytest.fixture
def sample_feats():
    """
    Fixture to provide a sample list of feats for testing.
    """
    feats = [
        {
            "name": "Power Attack",
            "description": "You can choose to take a -1 penalty on all melee attack rolls and combat maneuver checks to gain a +2 bonus on all melee damage rolls. This bonus to damage is increased by half (+50%) if you are making an attack with a two-handed weapon, a one handed weapon using two hands,  or a primary natural weapon that adds 1-1/2 times your Strength modifier on damage rolls. This bonus to damage is havled (-50%) if you are making an attack with an off-hand weapon or secondary natural weapon. When your base attack bonus reaches +4, and every 4 points thereafter, the penalty increases by -1 and the bonus to damage increases by +2. The effects of this feat last until your next turn. The bonus damage does not apply to touch sttacks or effects that do not deal hit point damage.",
            "prerequisite_stats": {"Str": 13},
            "prerequisite_feats": [],
            "prerequisite_level": 1,
        },
        {
            "name": "Cleave",
            "description": "As a standard action, you can make a single attack at your full base attack bonus against a foe within reach. If you hit, you deal damage normally and can make an additional attack (using your full base attack bonus)  against a foe that is adjacent to the first and also within reach. You can only make one additional attack per round with this feat. When you use this feat, you take a -2 penalty to your Armor Class until your next turn.",
            "prerequisite_feats": ["Power Attack"],
            "prerequisite_stats": {"Str": 13},
            "prerequisite_level": 1,
        },
        {
            "name": "Dodge",
            "description": "You gain a +1 dodge bonus to  your AC. A condition that makes you lose your Dex bonus to AC also makes you lose the benefits of this feat.",
            "prerequisite_stats": {"Dex": 13},
            "prerequisite_feats": [],
            "prerequisite_level": 1,
        },
    ]
    # Validate the sample feats against the schema
    for feat in feats:
        validate(instance=feat, schema=feat_schema)
    return feats

@pytest.fixture
def feats_tab(qtbot, monkeypatch, sample_feats):
    """
    Fixture to create a FeatsTab with sample feats for testing.
    Args:
        qtbot: QtBot instance
        monkeypatch: MonkeyPatch instance
        sample_feats: List of sample feats
    """
    from wotr_planner.ui import feats_tab as feats_tab_module
    # Patch the load_feats function to return the sample feats
    monkeypatch.setattr(feats_tab_module, "load_feats", lambda: sample_feats)
    c = Character()
    c.level = 1
    c.stats["Str"] = 13
    c.stats["Dex"] = 13
    tab = FeatsTab(c)
    qtbot.addWidget(tab)
    return tab

def test_update_feats_no_available_feats(qtbot, monkeypatch):
    """
    Test that the FeatsTab correctly handles the case where no feats are available due to stat prerequisites.
    Args:
        qtbot: QtBot instance
        monkeypatch: MonkeyPatch instance
    """
    from wotr_planner.ui import feats_tab as feats_tab_module
    # Patch the load_feats function to return a feat with high stat prerequisite
    monkeypatch.setattr(feats_tab_module, "load_feats", lambda: [
        {"name": "HighDexFeatDummy", "prerequisite_stats": {"Dex": 18}}
    ])
    c = Character()
    c.stats["Dex"] = 10
    tab = FeatsTab(c)
    qtbot.addWidget(tab)
    assert tab.feat_combo.count() == 1
    assert tab.feat_combo.itemText(0) == "No feats available placeholder text"

def test_show_feat_description_updates_box(feats_tab, sample_feats, qtbot):
    """
    Test that the FeatsTab correctly updates the description box when a feat is selected.
    Args:
        feats_tab: FeatsTab instance
        sample_feats: List of sample feats
        qtbot: QtBot instance
    """
    names = [f["name"] for f in sample_feats]
    idx = names.index("Power Attack")
    feats_tab.feat_combo.setCurrentIndex(idx)
    feats_tab.show_feat_description()
    text = feats_tab.description_box.toPlainText()
    assert "You can choose to take a -1 penalty on all melee attack rolls and combat maneuver checks to gain a +2 bonus on all melee damage rolls. This bonus to damage is increased by half (+50%) if you are making an attack with a two-handed weapon, a one handed weapon using two hands,  or a primary natural weapon that adds 1-1/2 times your Strength modifier on damage rolls. This bonus to damage is havled (-50%) if you are making an attack with an off-hand weapon or secondary natural weapon. When your base attack bonus reaches +4, and every 4 points thereafter, the penalty increases by -1 and the bonus to damage increases by +2. The effects of this feat last until your next turn. The bonus damage does not apply to touch sttacks or effects that do not deal hit point damage." in text

def test_show_selected_feat_description_updates_box(feats_tab, qtbot):
    """
    Test that the FeatsTab correctly updates the description box when a selected feat is chosen.
    Args:
        feats_tab: FeatsTab instance
        sample_feats: List of sample feats
        qtbot: QtBot instance
    """
    feats_tab.character.feats = [
        {
            "name": "Power Attack",
            "description": "You can choose to take a -1 penalty on all melee attack rolls and combat maneuver checks to gain a +2 bonus on all melee damage rolls. This bonus to damage is increased by half (+50%) if you are making an attack with a two-handed weapon, a one handed weapon using two hands,  or a primary natural weapon that adds 1-1/2 times your Strength modifier on damage rolls. This bonus to damage is havled (-50%) if you are making an attack with an off-hand weapon or secondary natural weapon. When your base attack bonus reaches +4, and every 4 points thereafter, the penalty increases by -1 and the bonus to damage increases by +2. The effects of this feat last until your next turn. The bonus damage does not apply to touch sttacks or effects that do not deal hit point damage."
        }
    ]
    feats_tab.refresh_selected_feats()
    item = feats_tab.selected_list.item(0)
    feats_tab.show_selected_feat_description(item)
    text = feats_tab.description_box.toPlainText()
    assert "You can choose to take a -1 penalty on all melee attack rolls and combat maneuver checks to gain a +2 bonus on all melee damage rolls. This bonus to damage is increased by half (+50%) if you are making an attack with a two-handed weapon, a one handed weapon using two hands,  or a primary natural weapon that adds 1-1/2 times your Strength modifier on damage rolls. This bonus to damage is havled (-50%) if you are making an attack with an off-hand weapon or secondary natural weapon. When your base attack bonus reaches +4, and every 4 points thereafter, the penalty increases by -1 and the bonus to damage increases by +2. The effects of this feat last until your next turn. The bonus damage does not apply to touch sttacks or effects that do not deal hit point damage." in text

def test_add_selected_feat_emits_signal(feats_tab, qtbot):
    """
    Test adding a selected feat emits the feats_changed signal.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    names = [feats_tab.feat_combo.itemText(i) for i in range(feats_tab.feat_combo.count())]
    idx = names.index("Power Attack")
    feats_tab.feat_combo.setCurrentIndex(idx)
    with qtbot.waitSignal(feats_tab.feats_changed, timeout=500):
        feats_tab.add_selected_feat()
    assert any(f["name"] == "Power Attack" for f in feats_tab.character.feats)
    assert "Power Attack" in [feats_tab.selected_list.item(i).text()
                              for i in range(feats_tab.selected_list.count())]
    
def test_add_selected_feat_blocked_slots(feats_tab, qtbot):
    """
    Test adding a selected feat is blocked when there are no available feat slots.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.total_feat_slots = lambda: 0 # Override to simulate no available slots
    names = [feats_tab.feat_combo.itemText(i) for i in range(feats_tab.feat_combo.count())]
    idx = names.index("Power Attack")
    feats_tab.feat_combo.setCurrentIndex(idx)
    with qtbot.assertNotEmitted(feats_tab.feats_changed):
        feats_tab.add_selected_feat()
    assert feats_tab.character.feats == []

def test_add_selected_feat_blocked_missing_prereq(feats_tab, qtbot):
    """
    Test adding a selected feat is blocked when prerequisites are not met.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.feats = [{"name": "Power Attack"}]
    feats_tab.update_feats()
    names = [feats_tab.feat_combo.itemText(i) for i in range(feats_tab.feat_combo.count())]
    assert "Cleave" in names
    idx = names.index("Cleave")
    feats_tab.feat_combo.setCurrentIndex(idx)
    feats_tab.character.feats = []
    with qtbot.assertNotEmitted(feats_tab.feats_changed):
        feats_tab.add_selected_feat()
    assert all(f["name"] != "Cleave" for f in feats_tab.character.feats)

def test_add_selected_feat_prereq(feats_tab, qtbot):
    """
    Test adding a selected feat with met prerequisites works correctly.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.feats = [{"name": "Power Attack"}]
    feats_tab.update_feats()
    names = [feats_tab.feat_combo.itemText(i) for i in range(feats_tab.feat_combo.count())]
    assert  "Cleave" in names
    idx = names.index("Cleave")
    feats_tab.feat_combo.setCurrentIndex(idx)
    with qtbot.waitSignal(feats_tab.feats_changed, timeout=500):
        feats_tab.add_selected_feat()
    assert any(f["name"] == "Cleave" for f in feats_tab.character.feats)

def test_add_selected_feat_blocked_stat(feats_tab, qtbot):
    """
    Test adding a selected feat is blocked when stat prerequisites are not met.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.stats["Str"] = 8 # Lower strength to block Power Attack
    names = [feats_tab.feat_combo.itemText(i) for i in range(feats_tab.feat_combo.count())]   
    idx = names.index("Power Attack")
    feats_tab.feat_combo.setCurrentIndex(idx)
    with qtbot.assertNotEmitted(feats_tab.feats_changed):
        feats_tab.add_selected_feat()
    assert feats_tab.character.feats == []

def test_add_selected_feat_blocked_level(feats_tab, qtbot):
    """
    Test adding a selected feat is blocked when level prerequisites are not met.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.feats = [{"name": "Power Attack"}]
    feats_tab.character.stats["Str"] = 13
    feats_tab.update_feats()
    names = [feats_tab.feat_combo.itemText(i) for i in range(feats_tab.feat_combo.count())]
    assert "Cleave" in names
    idx = names.index("Cleave")
    for f in feats_tab.feats:
        if f["name"] == "Cleave":
            f["prerequisite_level"] = 5 # Set level prerequisite higher than character level
    feats_tab.feat_combo.setCurrentIndex(idx)
    feats_tab.character.level = 1 # Ensure level is too low
    with qtbot.assertNotEmitted(feats_tab.feats_changed):
        feats_tab.add_selected_feat()
    assert all(f["name"] != "Cleave" for f in feats_tab.character.feats)

def test_add_selected_feat_no_duplicate(feats_tab, qtbot):
    """
    Test adding a selected feat is blocked when stat prerequisites are not met.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.feats = [next(f for f in feats_tab.feats if f["name"] == "Power Attack")]
    feats_tab.refresh_selected_feats()
    feats_tab.update_feats()
    names = [feats_tab.feat_combo.itemText(i) for i in range(feats_tab.feat_combo.count())]
    if "Power Attack" in names:
        idx = names.index("Power Attack")
        feats_tab.feat_combo.setCurrentIndex(idx)
    else:
        pytest.skip("Power Attack not available")
    with qtbot.assertNotEmitted(feats_tab.feats_changed):
        feats_tab.add_selected_feat()
    assert [f["name"] for f in feats_tab.character.feats].count("Power Attack") == 1 # No duplicates

def test_remove_selected_feat(feats_tab, qtbot):
    """
    Test removing a selected feat emits the feats_changed signal.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.feats = [next(f for f in feats_tab.feats if f["name"] == "Power Attack")]
    feats_tab.refresh_selected_feats()
    feats_tab.selected_list.setCurrentRow(0) # Select the first (and only) feat
    with qtbot.waitSignal(feats_tab.feats_changed, timeout=500):
        feats_tab.remove_selected_feat()
    assert feats_tab.character.feats == []
    assert feats_tab.selected_list.count() == 0 # No items left

def test_remove_selected_feat_no_selection_signal(feats_tab, qtbot):
    """
    Test removing a selected feat with no selection does not emit the feats_changed signal.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.character.feats = []
    feats_tab.refresh_selected_feats()
    with qtbot.assertNotEmitted(feats_tab.feats_changed):
        feats_tab.remove_selected_feat()

def test_show_selected_feat_description_missing(feats_tab, qtbot):
    """
    Test showing a description for a missing feat does not crash.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.selected_list.addItem("Nonexistent Feat")
    item = feats_tab.selected_list.item(feats_tab.selected_list.count() - 1)
    feats_tab.show_selected_feat_description(item)
    assert feats_tab.description_box.toPlainText() == ""

def test_selected_not_chosen_feat(feats_tab, qtbot):
    """
    Test adding a selected feat that is not in the available feats list.
    Args:
        feats_tab: FeatsTab instance
        qtbot: QtBot instance
    """
    feats_tab.feat_combo.addItem("FakeFeat")
    feats_tab.feat_combo.setCurrentText("FakeFeat")
    with qtbot.assertNotEmitted(feats_tab.feats_changed):
        feats_tab.add_selected_feat()
    assert feats_tab.character.feats == []
