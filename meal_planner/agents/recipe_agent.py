from meal_planner.models import Ingredient, MenuProposal, Recipe, RecipePackage, RecipeStep, RecipeVariant, UserRequest


class RecipeAgent:
    """Génère les recettes et les variantes utiles."""

    def generate_recipes(self, menu: MenuProposal, request: UserRequest) -> list[RecipePackage]:
        packages: list[RecipePackage] = []

        for item in menu.menu_items:
            recipe = Recipe(
                name=item.name,
                category=item.category,
                ingredients=[
                    Ingredient(name="carotte", quantity="500", unit="g"),
                    Ingredient(name="courgette", quantity="300", unit="g"),
                    Ingredient(name="oignon", quantity="1", unit="unité"),
                ],
                steps=[
                    RecipeStep(order=1, description="Préparer les légumes."),
                    RecipeStep(order=2, description="Faire cuire doucement."),
                    RecipeStep(order=3, description="Assaisonner et servir."),
                ],
                prep_time_minutes=20,
                cook_time_minutes=30,
                equipment=["casserole", "planche à découper"],
                difficulty="facile",
                variants=[
                    RecipeVariant(
                        type="végétarien",
                        description="Version sans viande.",
                        adapted_ingredients=["quinoa", "pois chiches"],
                    ),
                    RecipeVariant(
                        type="halal",
                        description="Version compatible halal.",
                        adapted_ingredients=["viande halal"],
                    ),
                ],
            )

            packages.append(
                RecipePackage(
                    menu_item_name=item.name,
                    recipe=recipe,
                    alternatives=[],
                )
            )

        return packages
