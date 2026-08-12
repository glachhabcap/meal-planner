from meal_planner.agents.orchestrator import OrchestratorAgent


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
