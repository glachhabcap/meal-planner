from meal_planner.agents.orchestrator import OrchestratorAgent
from meal_planner.models import MenuItem, MenuProposal, PlanningResult, PlanningStep, Recipe, RecipePackage, RecipeStep, ShoppingResult, ShoppingItem


def test_orchestrator_generates_final_plan():
    raw_text = (
        "Je reçois 6 personnes samedi soir. "
        "Budget 60€. Maximum 1h30 de préparation. "
        "Une personne est végétarienne, une autre mange halal. "
        "Je souhaite privilégier les légumes de saison."
    )

    result = OrchestratorAgent().run(raw_text)

    assert result.menu is not None
    assert result.recipes
    assert result.shopping is not None
    assert result.planning is not None
    assert isinstance(result.final_summary, str)


def test_orchestrator_extracts_constraints_from_raw_text():
    raw_text = (
        "Pour 8 personnes, budget 30€, maximum 45 minutes, "
        "végétarienne et halal, légumes de saison, dîner de famille."
    )

    request = OrchestratorAgent().analyze_request(raw_text)

    assert request.guests == 8
    assert request.budget_eur == 30
    assert request.max_prep_minutes == 45
    assert "végétarienne" in request.dietary_constraints
    assert "halal" in request.dietary_constraints
    assert request.occasion == "dîner"
    assert any("saison" in preference.lower() for preference in request.seasonal_preferences)


def test_orchestrator_warns_about_budget_timing_and_dietary_issues():
    orchestrator = OrchestratorAgent()
    request = orchestrator.analyze_request(
        "Pour 10 personnes, budget 10€, maximum 20 minutes, végétarienne."
    )

    menu = MenuProposal(
        menu_items=[
            MenuItem(
                name="Poulet halal",
                category="plat",
                description="Plat non compatible.",
                justification="Pas adapté.",
            )
        ],
        summary="menu de test",
    )
    recipes = [
        RecipePackage(
            menu_item_name="Poulet halal",
            recipe=Recipe(
                name="Poulet halal",
                category="plat",
                ingredients=[],
                steps=[RecipeStep(order=1, description="Cuire")],
                prep_time_minutes=15,
                cook_time_minutes=20,
                equipment=[],
                difficulty="facile",
            ),
            alternatives=[],
        )
    ]
    shopping = ShoppingResult(
        items=[ShoppingItem(ingredient="poulet", quantity="1", estimated_price_eur=35)],
        total_estimated_eur=35,
        budget_ok=False,
        recommended_alternatives=["acheter moins de viande"],
    )
    planning = PlanningResult(
        schedule=[PlanningStep(title="Préparation", start_minute=0, end_minute=30, dependencies=[])],
        total_duration_minutes=30,
        realistic_within_limit=False,
        comments=["Le temps dépasse la limite."],
    )

    warnings = orchestrator.validate_results(menu, recipes, shopping, planning, request)

    assert any("budget" in warning.lower() for warning in warnings)
    assert any("temps" in warning.lower() or "planning" in warning.lower() for warning in warnings)
    assert any("régime" in warning.lower() or "contrainte" in warning.lower() for warning in warnings)
