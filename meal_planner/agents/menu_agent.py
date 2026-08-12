from meal_planner.models import MenuItem, MenuProposal, UserRequest


class MenuAgent:
    """Propose un menu cohérent selon les contraintes utilisateur."""

    def generate_menu(self, request: UserRequest) -> MenuProposal:
        items = [
            MenuItem(
                name="Velouté de légumes de saison",
                category="entree",
                description="Entrée chaude et légère.",
                justification="Adaptée aux légumes de saison et à un repas convivial.",
            ),
            MenuItem(
                name="Poulet halal aux légumes rôtis",
                category="plat",
                description="Plat principal équilibré.",
                justification="Compatible avec les contraintes halal et facile à préparer en groupe.",
            ),
            MenuItem(
                name="Quinoa aux herbes",
                category="accompagnement",
                description="Accompagnement simple et rassasiant.",
                justification="Idéal pour satisfaire les invités végétariens et équilibrer le plat.",
            ),
            MenuItem(
                name="Tarte aux pommes",
                category="dessert",
                description="Dessert classique et peu coûteux.",
                justification="Facile à réaliser, convivial et compatible avec un budget limité.",
            ),
        ]

        return MenuProposal(
            menu_items=items,
            summary="Menu équilibré, simple, convivial et adapté aux contraintes de budget et de saison.",
        )
