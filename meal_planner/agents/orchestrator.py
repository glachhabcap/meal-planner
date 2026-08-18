import re

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

    @staticmethod
    def _extract_guests(raw_text: str) -> int:
        match = re.search(r"(?:pour\s+)?(\d+)\s*personnes?", raw_text.lower())
        if match:
            return int(match.group(1))
        return 6

    @staticmethod
    def _extract_budget_eur(raw_text: str) -> float:
        match = re.search(r"(?:budget|budg(?:et)?)\s*(?:de\s*)?(\d+(?:[.,]\d+)?)\s*€", raw_text.lower())
        if match:
            return float(match.group(1).replace(",", "."))
        match = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:eur|euros?)", raw_text.lower())
        if match:
            return float(match.group(1).replace(",", "."))
        return 60.0

    @staticmethod
    def _extract_max_prep_minutes(raw_text: str) -> int:
        normalized = raw_text.lower()

        hours_match = re.search(r"(\d+)\s*h(?:ours?)?(?:\s*(\d+))?", normalized)
        if hours_match:
            hours = int(hours_match.group(1))
            minutes = int(hours_match.group(2) or 0)
            return hours * 60 + minutes

        minutes_match = re.search(r"(?:maximum|max|au plus|limite)\s*(\d+)\s*(?:minutes|min|mins?)", normalized)
        if minutes_match:
            return int(minutes_match.group(1))

        minutes_match = re.search(r"(\d+)\s*(?:minutes|min|mins?)", normalized)
        if minutes_match:
            return int(minutes_match.group(1))

        return 90

    @staticmethod
    def _extract_dietary_constraints(raw_text: str) -> list[str]:
        normalized = raw_text.lower()
        constraints: list[str] = []

        if any(keyword in normalized for keyword in ["végétarien", "vegetarien", "végétarienne", "vegetarienne"]):
            constraints.append("végétarienne")
        if any(keyword in normalized for keyword in ["halal", "hallal"]):
            constraints.append("halal")
        if any(keyword in normalized for keyword in ["sans gluten", "gluten free", "sans-gluten"]):
            constraints.append("sans gluten")
        if any(keyword in normalized for keyword in ["sans lactose", "lactose free", "sans-lactose"]):
            constraints.append("sans lactose")

        return constraints

    @staticmethod
    def _extract_seasonal_preferences(raw_text: str) -> list[str]:
        normalized = raw_text.lower()
        preferences: list[str] = []

        if any(keyword in normalized for keyword in ["légumes de saison", "legumes de saison", "legume de saison", "saison"]):
            preferences.append("légumes de saison")
        if "printemps" in normalized:
            preferences.append("printemps")
        if "automne" in normalized:
            preferences.append("automne")
        if "hiver" in normalized:
            preferences.append("hiver")
        if "été" in normalized or "ete" in normalized:
            preferences.append("été")

        return preferences

    @staticmethod
    def _extract_occasion(raw_text: str) -> str:
        normalized = raw_text.lower()
        if "déjeuner" in normalized or "dejeuner" in normalized:
            return "déjeuner"
        if "brunch" in normalized:
            return "brunch"
        if "repas" in normalized or "dîner" in normalized or "diner" in normalized or "soir" in normalized:
            return "dîner"
        return "dîner"

    @staticmethod
    def _extract_notes(raw_text: str) -> list[str]:
        notes: list[str] = []
        normalized = raw_text.lower()

        if "famille" in normalized:
            notes.append("repas de famille")
        if "convivial" in normalized or "amis" in normalized:
            notes.append("repas convivial")
        if "simple" in normalized or "facile" in normalized:
            notes.append("préparation simple")

        return notes

    def analyze_request(self, raw_text: str) -> UserRequest:
        """Transforme le texte utilisateur en objet structuré."""
        return UserRequest(
            raw_text=raw_text,
            guests=self._extract_guests(raw_text),
            occasion=self._extract_occasion(raw_text),
            budget_eur=self._extract_budget_eur(raw_text),
            max_prep_minutes=self._extract_max_prep_minutes(raw_text),
            dietary_constraints=self._extract_dietary_constraints(raw_text),
            seasonal_preferences=self._extract_seasonal_preferences(raw_text),
            notes=self._extract_notes(raw_text),
        )

    def validate_results(
        self,
        menu: MenuProposal,
        recipes,
        shopping: ShoppingResult,
        planning: PlanningResult,
        request: UserRequest | None = None,
    ) -> list[str]:
        warnings: list[str] = []

        if not menu or not menu.menu_items:
            warnings.append("Le menu est vide.")

        if not recipes:
            warnings.append("Aucune recette n'a été générée.")

        if not shopping.budget_ok:
            warnings.append("Le budget estimé dépasse le budget cible.")

        if not planning.realistic_within_limit:
            warnings.append("Le planning semble trop long pour le temps disponible.")

        if request and request.dietary_constraints:
            menu_text = " ".join(
                f"{item.name} {item.description} {item.justification}".lower()
                for item in menu.menu_items
            )
            recipe_text = " ".join(
                (package.recipe.name + " " + " ".join(variant.type for variant in package.recipe.variants)).lower()
                for package in recipes
            )
            compatible_text = f"{menu_text} {recipe_text}"
            dietary_issues: list[str] = []

            if "végétarienne" in request.dietary_constraints:
                forbidden_terms = ["poulet", "boeuf", "bœuf", "porc", "viande", "poisson", "canard"]
                if any(term in compatible_text for term in forbidden_terms) and not any(term in compatible_text for term in ["végétar", "vegetar", "veggie"]):
                    dietary_issues.append("végétarienne")

            if "halal" in request.dietary_constraints:
                if "porc" in compatible_text and not "halal" in compatible_text:
                    dietary_issues.append("halal")
                elif any(term in compatible_text for term in ["porc", "alcool", "charcuterie"]) and "halal" not in compatible_text:
                    dietary_issues.append("halal")

            if "sans gluten" in request.dietary_constraints:
                if any(term in compatible_text for term in ["pain", "blé", "ble", "farine", "pate"]) and "sans gluten" not in compatible_text:
                    dietary_issues.append("sans gluten")

            if dietary_issues:
                warnings.append(
                    "Le menu n'est pas compatible avec les contraintes alimentaires : "
                    + ", ".join(dietary_issues)
                    + "."
                )

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

        warnings = self.validate_results(menu, recipes, shopping, planning, request)
        final_summary = (
            "Menu validé avec les contraintes et le planning principal."
            if not warnings
            else "Le plan a été validé avec des avertissements à corriger."
        )

        final_plan = FinalMealPlan(
            menu=menu,
            recipes=recipes,
            shopping=shopping,
            planning=planning,
            warnings=warnings,
            final_summary=final_summary,
        )

        iteration = 1
        while (
            any(
                keyword in warning.lower()
                for warning in warnings
                for keyword in ["budget", "planning", "temps", "régime", "contrainte"]
            )
            and iteration < self.MAX_ITERATIONS
        ):
            menu = menu_agent.generate_menu(request)
            recipes = recipe_agent.generate_recipes(menu, request)
            shopping = shopping_agent.compute_shopping(recipes, request)
            planning = organization_agent.build_plan(recipes, request)

            warnings = self.validate_results(menu, recipes, shopping, planning, request)
            final_summary = "Plan recalculé après ajustement du budget ou du planning."

            final_plan = FinalMealPlan(
                menu=menu,
                recipes=recipes,
                shopping=shopping,
                planning=planning,
                warnings=warnings,
                final_summary=final_summary,
            )
            iteration += 1

        return final_plan
