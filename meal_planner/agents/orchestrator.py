from meal_planner.agents.menu_agent import MenuAgent
from meal_planner.agents.recipe_agent import RecipeAgent
from meal_planner.agents.shopping_budget_agent import ShoppingBudgetAgent
from meal_planner.agents.organization_agent import OrganizationAgent
from meal_planner.config import MAX_AGENT_ITERATIONS
from meal_planner.models import (
    FinalMealPlan,
    MenuProposal,
    PlanningResult,
    ShoppingResult,
    UserRequest,
)


class OrchestratorAgent:
    """Agent central qui pilote le flux global du projet.

    Rôle pédagogique :
    - extraire les contraintes de la demande ;
    - appeler les autres agents ;
    - valider la cohérence globale ;
    - relancer un flux si nécessaire ;
    - produire le résultat final.
    """

    MAX_ITERATIONS = MAX_AGENT_ITERATIONS

    def analyze_request(self, raw_text: str) -> UserRequest:
        """Transforme le texte utilisateur en objet structuré."""
        return UserRequest(
            raw_text=raw_text,
            guests=6,
            occasion="dîner",
            budget_eur=60,
            max_prep_minutes=90,
            dietary_constraints=["végétarienne", "halal"],
            seasonal_preferences=["légumes de saison"],
            notes=["repas convivial", "préparation simple"],
        )

    def validate_results(
        self,
        menu: MenuProposal,
        recipes,
        shopping: ShoppingResult,
        planning: PlanningResult,
    ) -> list[str]:
        warnings: list[str] = []

        if not menu.menu_items:
            warnings.append("Le menu est vide.")

        if not recipes:
            warnings.append("Aucune recette n'a été générée.")

        if not shopping.budget_ok:
            warnings.append("Le budget estimé dépasse le budget cible.")

        if not planning.realistic_within_limit:
            warnings.append("Le planning semble trop long pour le temps disponible.")

        return warnings

    def run(self, raw_text: str) -> FinalMealPlan:
        """Exécute le pipeline principal du projet."""
        request = self.analyze_request(raw_text)
        menu_agent = MenuAgent()
        recipe_agent = RecipeAgent()
        shopping_agent = ShoppingBudgetAgent()
        organization_agent = OrganizationAgent()

        menu = menu_agent.generate_menu(request)
        recipes = recipe_agent.generate_recipes(menu, request)
        shopping = shopping_agent.compute_shopping(recipes, request)
        planning = organization_agent.build_plan(recipes, request)

        warnings = self.validate_results(menu, recipes, shopping, planning)

        final_plan = FinalMealPlan(
            menu=menu,
            recipes=recipes,
            shopping=shopping,
            planning=planning,
            warnings=warnings,
            final_summary="Menu validé avec les contraintes et le planning principal.",
        )

        iteration = 1
        while (
            (not shopping.budget_ok or not planning.realistic_within_limit)
            and iteration < self.MAX_ITERATIONS
        ):
            menu = menu_agent.generate_menu(request)
            recipes = recipe_agent.generate_recipes(menu, request)
            shopping = shopping_agent.compute_shopping(recipes, request)
            planning = organization_agent.build_plan(recipes, request)

            warnings = self.validate_results(menu, recipes, shopping, planning)

            final_plan = FinalMealPlan(
                menu=menu,
                recipes=recipes,
                shopping=shopping,
                planning=planning,
                warnings=warnings,
                final_summary="Plan recalculé après ajustement du budget ou du planning.",
            )
            iteration += 1

        return final_plan
