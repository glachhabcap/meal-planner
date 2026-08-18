from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    """Demande initiale de l'utilisateur en langage naturel structurée."""

    raw_text: str = Field(..., description="Demande utilisateur en langage naturel")
    guests: int = Field(..., ge=1)
    occasion: str = Field(default="dîner")
    budget_eur: float = Field(..., ge=0)
    max_prep_minutes: int = Field(..., ge=10)
    dietary_constraints: List[str] = Field(default_factory=list)
    seasonal_preferences: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class MenuItem(BaseModel):
    """Un élément d'un menu."""

    name: str
    category: str
    description: str
    justification: str


class MenuProposal(BaseModel):
    """Menu complet proposé par le Menu Agent."""

    menu_items: List[MenuItem]
    summary: str


class Ingredient(BaseModel):
    """Ingrédient d'une recette."""

    name: str
    quantity: str
    unit: Optional[str] = None
    note: Optional[str] = None



class RecipeStep(BaseModel):
    """Étape de préparation d'une recette."""

    order: int
    description: str


class RecipeVariant(BaseModel):
    """Variante d'une recette adaptée à une contrainte."""

    type: str
    description: str
    adapted_ingredients: List[str] = Field(default_factory=list)


class Recipe(BaseModel):
    """Recette complète associée à un menu."""

    name: str
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    portions: int = 1
    advice: Optional[str] = None
    calories_kcal: Optional[int] = None
    proteins_g: Optional[int] = None
    carbs_g: Optional[int] = None
    lipids_g: Optional[int] = None
    ingredients: List[Ingredient]
    steps: List[RecipeStep]
    prep_time_minutes: int
    cook_time_minutes: int
    total_time_minutes: Optional[int] = None
    equipment: List[str]
    difficulty: str
    beginner_friendly: bool = False
    variants: List[RecipeVariant] = Field(default_factory=list)


class RecipePackage(BaseModel):
    """Recette et alternatives associées à un élément du menu."""

    menu_item_name: str
    recipe: Recipe
    alternatives: List[Recipe] = Field(default_factory=list)


class ShoppingItem(BaseModel):
    """Produit à acheter estimé pour la recette."""

    ingredient: str
    quantity: str
    unit: Optional[str] = None
    estimated_price_eur: float


class ShoppingResult(BaseModel):
    """Résultat de l'agrégation des achats et du budget."""

    items: List[ShoppingItem]
    total_estimated_eur: float
    budget_ok: bool
    budget_remaining_eur: float = 0.0
    budget_used_pct: float = 0.0
    product_most_expensive: str = ""
    product_least_expensive: str = ""
    article_count: int = 0
    average_price_eur: float = 0.0
    recommended_alternatives: List[str] = Field(default_factory=list)
    status_icon: str = "🟢"
    status_label: str = "Budget respecté"
    status_color: str = "green"


class PlanningStep(BaseModel):
    """Étape de préparation d'un planning."""

    title: str
    start_minute: int
    end_minute: int
    dependencies: List[str] = Field(default_factory=list)
    parallelizable: bool = False


class PlanningResult(BaseModel):
    """Planning final d'organisation de la préparation."""

    schedule: List[PlanningStep]
    total_duration_minutes: int
    realistic_within_limit: bool
    comments: List[str] = Field(default_factory=list)


class FinalMealPlan(BaseModel):
    """Résultat complet du repas."""

    menu: MenuProposal
    recipes: List[RecipePackage]
    shopping: ShoppingResult
    planning: PlanningResult
    warnings: List[str] = Field(default_factory=list)
    final_summary: str
