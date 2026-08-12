from meal_planner.agents.menu_agent import MenuAgent
from meal_planner.models import UserRequest


def test_menu_agent_returns_menu():
    request = UserRequest(
        raw_text="test",
        guests=4,
        budget_eur=50,
        max_prep_minutes=60,
        dietary_constraints=["végétarienne"],
        seasonal_preferences=["légumes de saison"],
    )

    menu = MenuAgent().generate_menu(request)

    assert menu.menu_items
    assert len(menu.menu_items) >= 4
    assert menu.summary
