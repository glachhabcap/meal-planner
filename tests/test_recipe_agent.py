from meal_planner.agents.recipe_agent import RecipeAgent
from meal_planner.models import MenuProposal, MenuItem, UserRequest


def test_recipe_agent_generates_packages():
    request = UserRequest(
        raw_text="test",
        guests=4,
        budget_eur=50,
        max_prep_minutes=60,
        dietary_constraints=["halal"],
        seasonal_preferences=["légumes de saison"],
    )

    menu = MenuProposal(
        menu_items=[
            MenuItem(
                name="Plat principal",
                category="plat",
                description="test",
                justification="test",
            )
        ],
        summary="menu test",
    )

    recipes = RecipeAgent().generate_recipes(menu, request)

    assert len(recipes) == 1
    assert recipes[0].recipe.ingredients
    assert recipes[0].recipe.steps
