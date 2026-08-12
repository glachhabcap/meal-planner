from meal_planner.models import RecipePackage, ShoppingItem, ShoppingResult, UserRequest


class ShoppingBudgetAgent:
    """Agrège les achats et calcule le budget estimé."""

    def compute_shopping(self, recipes: list[RecipePackage], request: UserRequest) -> ShoppingResult:
        items = [
            ShoppingItem(
                ingredient="carotte",
                quantity="500",
                unit="g",
                estimated_price_eur=2.5,
            ),
            ShoppingItem(
                ingredient="courgette",
                quantity="300",
                unit="g",
                estimated_price_eur=2.0,
            ),
            ShoppingItem(
                ingredient="oignon",
                quantity="1",
                unit="unité",
                estimated_price_eur=0.8,
            ),
        ]

        total = sum(item.estimated_price_eur for item in items)

        return ShoppingResult(
            items=items,
            total_estimated_eur=round(total, 2),
            budget_ok=total <= request.budget_eur,
            recommended_alternatives=[
                "acheter les légumes de saison",
                "préférer les légumes locaux",
            ],
        )
