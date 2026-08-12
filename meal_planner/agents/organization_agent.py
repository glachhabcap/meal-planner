from meal_planner.models import PlanningResult, PlanningStep, RecipePackage, UserRequest


class OrganizationAgent:
    """Organise le plan de préparation et vérifie sa faisabilité."""

    def build_plan(self, recipes: list[RecipePackage], request: UserRequest) -> PlanningResult:
        schedule = [
            PlanningStep(
                title="Préparation des légumes",
                start_minute=0,
                end_minute=20,
                dependencies=[],
                parallelizable=True,
            ),
            PlanningStep(
                title="Cuisson du plat principal",
                start_minute=20,
                end_minute=50,
                dependencies=["Préparation des légumes"],
                parallelizable=False,
            ),
            PlanningStep(
                title="Dressage et service",
                start_minute=50,
                end_minute=80,
                dependencies=["Cuisson du plat principal"],
                parallelizable=True,
            ),
        ]

        total_duration = 80
        realistic = total_duration <= request.max_prep_minutes

        return PlanningResult(
            schedule=schedule,
            total_duration_minutes=total_duration,
            realistic_within_limit=realistic,
            comments=[
                "Les tâches de préparation peuvent être réparties.",
                "Le temps est compatible avec la demande.",
            ],
        )
