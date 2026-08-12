from meal_planner.agents.shopping_budget_agent import ShoppingBudgetAgent
from meal_planner.models import Ingredient, Recipe, RecipePackage, RecipeStep, UserRequest


def test_shopping_budget_agent_returns_total():
    request = UserRequest(
        raw_text="test",
        guests=4,
        budget_eur=50,
        max_prep_minutes=60,
        dietary_constraints=[],
        seasonal_preferences=[],
    )

    recipe = Recipe(
        name="Plat test",
        category="plat",
        ingredients=[Ingredient(name="carotte", quantity="500", unit="g")],
        steps=[RecipeStep(order=1, description="Cuire")],
        prep_time_minutes=20,
        cook_time_minutes=25,
        equipment=["casserole"],
        difficulty="facile",
    )

    shopping = ShoppingBudgetAgent().compute_shopping(
        [RecipePackage(menu_item_name="Plat test", recipe=recipe)],
        request,
    )

    assert shopping.total_estimated_eur >= 0
    assert isinstance(shopping.budget_ok, bool)
