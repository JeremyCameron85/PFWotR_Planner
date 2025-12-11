import pytest
from wotr_planner.ui.stats_tab import StatsTab
from wotr_planner.models.character import Character

def test_point_cost_values():
    """
    Test the point cost calculation for various stat values.
    - Verify that the point cost matches expected values for given stats.
    """
    assert StatsTab.point_cost(7) == -4
    assert StatsTab.point_cost(10) ==  0
    assert StatsTab.point_cost(14) == 5
    assert StatsTab.point_cost(18) == 17

def test_total_points_spent(qtbot):
    """
    Test the total points spent calculation in the StatsTab.
    - Create a character and set various stats.
    - Verify that the total points spent is calculated correctly.
    - Uses qtbot to handle the StatsTab widget.
    Args:
        qtbot: pytest-qt fixture for handling Qt widgets.
    """
    char = Character(
        char_class={"name": "Fighter", "skill_points": 2},
        race={"name": "Human"}
    )
    stats_tab = StatsTab(char)
    qtbot.addWidget(stats_tab) # Add the widget to qtbot for proper handling

    # Initial total points spent should be 0
    assert stats_tab.total_points_spent() == 0
    
    # Set stats and verify total points spent
    char.point_buy_stats["Str"]  = 14
    assert stats_tab.total_points_spent()  == 5