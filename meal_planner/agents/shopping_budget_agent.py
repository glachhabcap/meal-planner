from meal_planner.models import RecipePackage, ShoppingItem, ShoppingResult, UserRequest


class ShoppingBudgetAgent:
    """Agrège les achats et calcule le budget estimé."""

    @staticmethod
    def _parse_quantity(quantity: str) -> float:
        try:
            return float(str(quantity).replace(",", ".").strip())
        except (TypeError, ValueError):
            return 1.0

    @staticmethod
    def _unit_factor(unit: str | None) -> float:
        normalized = (unit or "").lower()
        if normalized in {"g", "gr", "gramme", "grammes"}:
            return 0.01
        if normalized in {"kg", "kilo", "kilogramme", "kilogrammes"}:
            return 1.0
        if normalized in {"l", "litre", "litres", "ml", "millilitre", "millilitres"}:
            return 0.7
        return 1.0

    @staticmethod
    def _ingredient_base_price(name: str) -> float:
        prices = {
            "carotte": 2.8,
            "courgette": 2.4,
            "oignon": 1.7,
            "pommes": 2.2,
            "tomate": 3.0,
            "tomates": 3.0,
            "poivron": 2.9,
            "aubergine": 3.2,
            "courgettes": 2.4,
            "laitue": 2.0,
            "riz": 2.6,
            "poulet": 9.5,
            "poisson": 12.0,
            "fromage": 8.5,
            "yaourt": 2.1,
            "pain": 2.7,
            "oeuf": 2.4,
            "œuf": 2.4,
            "œufs": 2.4,
            "oeufs": 2.4,
            "pois chiches": 2.9,
            "lentilles": 2.4,
            "huile": 4.3,
            "beurre": 4.8,
            "citron": 1.8,
            "ail": 1.5,
            "persil": 1.4,
            "champignon": 3.5,
            "champignons": 3.5,
            "banane": 2.0,
            "pomme": 1.9,
            "yaourts": 2.1,
        }
        return prices.get(name.lower(), 2.5)

    def compute_shopping(self, recipes: list[RecipePackage], request: UserRequest) -> ShoppingResult:
        aggregated: dict[str, dict[str, float | str]] = {}

        for recipe_package in recipes:
            for ingredient in recipe_package.recipe.ingredients:
                key = ingredient.name.lower()
                quantity = self._parse_quantity(ingredient.quantity)
                unit_factor = self._unit_factor(ingredient.unit)
                unit = ingredient.unit or "unité"
                item_price = self._ingredient_base_price(ingredient.name) * quantity * unit_factor

                if key not in aggregated:
                    aggregated[key] = {
                        "ingredient": ingredient.name,
                        "quantity": quantity,
                        "unit": unit,
                        "estimated_price_eur": item_price,
                    }
                else:
                    aggregated[key]["quantity"] = float(aggregated[key]["quantity"]) + quantity
                    aggregated[key]["estimated_price_eur"] = float(aggregated[key]["estimated_price_eur"]) + item_price

        items = [
            ShoppingItem(
                ingredient=str(data["ingredient"]),
                quantity=str(round(float(data["quantity"]), 2)),
                unit=str(data["unit"]),
                estimated_price_eur=round(float(data["estimated_price_eur"]), 2),
            )
            for data in aggregated.values()
        ]

        total = round(sum(item.estimated_price_eur for item in items), 2)
        budget_remaining = round(request.budget_eur - total, 2)
        budget_used_pct = round((total / request.budget_eur * 100), 2) if request.budget_eur else 0.0
        most_expensive = max(items, key=lambda item: item.estimated_price_eur, default=None)
        cheapest = min(items, key=lambda item: item.estimated_price_eur, default=None)

        if not items:
            items = [ShoppingItem(ingredient="Aucun ingredient", quantity="0", unit="", estimated_price_eur=0.0)]
            most_expensive = items[0]
            cheapest = items[0]

        alternatives = [
            "acheter les légumes de saison",
            "préférer les produits locaux",
            "choisir les marques distributeur",
        ]
        if total > request.budget_eur:
            alternatives.insert(0, "remplacer les produits les plus chers par des alternatives économiques")

        status_icon = "🟢"
        status_label = "Budget respecté"
        if total > request.budget_eur:
            status_icon = "🔴"
            status_label = "Budget dépassé"
        elif budget_used_pct >= 75:
            status_icon = "🟠"
            status_label = "Vigilance"

        result = ShoppingResult(
            items=items,
            total_estimated_eur=total,
            budget_ok=total <= request.budget_eur,
            budget_remaining_eur=budget_remaining,
            budget_used_pct=budget_used_pct,
            product_most_expensive=most_expensive.ingredient if most_expensive else "Aucun",
            product_least_expensive=cheapest.ingredient if cheapest else "Aucun",
            article_count=len(items),
            average_price_eur=round(total / len(items), 2) if items else 0.0,
            recommended_alternatives=alternatives,
        )

        result.status_icon = status_icon
        result.status_label = status_label
        result.status_color = "green" if total <= request.budget_eur else "red"
        if budget_used_pct >= 75 and total <= request.budget_eur:
            result.status_color = "orange"

        return result
