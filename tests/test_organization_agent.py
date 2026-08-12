from meal_planner.agents.organization_agent import OrganizationAgent
from meal_planner.models import Ingredient, Recipe, RecipePackage, RecipeStep, UserRequest


def test_organization_agent_builds_planning():
    request = UserRequest(
        raw_text="test planning",
        guests=4,
        budget_eur=50,
        max_prep_minutes=90,
        dietary_constraints=[],
        seasonal_preferences=[],
    )

    recipe = Recipe(
        name="Plat test",
        category="plat",
        ingredients=[Ingredient(name="courgette", quantity="500", unit="g")],
        steps=[RecipeStep(order=1, description="Cuire")],
        prep_time_minutes=15,
        cook_time_minutes=25,
        equipment=["poêle"],
        difficulty="facile",
    )

    planning = OrganizationAgent().build_plan(
        [RecipePackage(menu_item_name="Plat test", recipe=recipe)],
        request,
    )

    assert planning.schedule
    assert planning.total_duration_minutes > 0
    assert isinstance(planning.realistic_within_limit, bool)
