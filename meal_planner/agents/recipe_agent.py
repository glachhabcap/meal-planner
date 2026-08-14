import json
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from meal_planner.models import (
    Ingredient,
    MenuProposal,
    Recipe,
    RecipePackage,
    RecipeStep,
    RecipeVariant,
    UserRequest,
)


def _load_templates() -> list[dict]:
    # recipe_templates.json is located at the project root `data/` directory
    path = Path(__file__).parents[2] / "data" / "recipe_templates.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("templates", [])
    except Exception:
        return []


TEMPLATES = _load_templates()


def _estimate_quantity_per_guest(ingredient_name: str) -> tuple[int, str]:
    veg = {
        "carotte": 100,
        "courgette": 100,
        "oignon": 50,
        "poireau": 80,
        "poivron": 100,
        "aubergine": 120,
        "tomate": 80,
        "persil": 5,
        "pommes": 150,
        "poires": 150,
    }
    protein = {"poulet": 180, "poisson": 150, "oeuf": 1}
    grain = {"quinoa": 60, "riz": 60}
    spices = {"cannelle": 1, "sel": 1, "poivre": 1, "sucre": 15, "farine": 60, "beurre": 30}

    name = ingredient_name.lower()
    if name in veg:
        return veg[name], "g"
    if name in protein:
        return protein[name], "g" if name != "oeuf" else "unité"
    if name in grain:
        return grain[name], "g"
    if name in spices:
        return spices[name], "g"
    if name in ("lait", "eau", "bouillon"):
        return 100, "ml"
    return 50, "g"


def _choose_template_for(item_name: str, category: str) -> Optional[dict]:
    name = item_name.lower()
    stopwords = {"de", "des", "la", "le", "les", "aux", "et", "du"}
    def words(s: str):
        return [w for w in s.lower().replace("é", "e").split() if w and w not in stopwords]

    item_words = set(words(item_name))
    best = None
    best_score = 0
    for t in TEMPLATES:
        t_words = set(words(t.get("name", "")))
        score = len(item_words & t_words)
        # bonus if category matches
        if t.get("category") == category:
            score += 1
        if score > best_score:
            best_score = score
            best = t
    return best


def _image_for_recipe(recipe_name: str) -> str:
    # Representative image for the recipe (unsplash query)
    name = quote(recipe_name)
    return f"https://source.unsplash.com/800x600/?{name},food,dish"


def _steps_for_template(template_name: str, category: str) -> list[RecipeStep]:
    name = template_name.lower()
    steps: list[RecipeStep] = []
    order = 1
    if "velout" in name or "soupe" in name:
        steps.append(RecipeStep(order=order, description="Laver et découper les légumes."))
        order += 1
        steps.append(RecipeStep(order=order, description="Faire revenir les légumes 5–7 min dans un peu d'huile."))
        order += 1
        steps.append(RecipeStep(order=order, description="Ajouter du bouillon, cuire 15–20 min jusqu'à tendreté."))
        order += 1
        steps.append(RecipeStep(order=order, description="Mixer au mixeur plongeant ou blender jusqu'à obtenir une texture lisse."))
        order += 1
        steps.append(RecipeStep(order=order, description="Assaisonner et servir chaud."))
        return steps

    if "salade" in name:
        steps.append(RecipeStep(order=order, description="Cuire le quinoa ou céréales selon instructions."))
        order += 1
        steps.append(RecipeStep(order=order, description="Couper les légumes et herbes; préparer la vinaigrette."))
        order += 1
        steps.append(RecipeStep(order=order, description="Mélanger et rectifier l'assaisonnement."))
        return steps

    if "tarte" in name or "dessert" in category or "tarte" in category:
        steps.append(RecipeStep(order=order, description="Préparer la pâte si nécessaire et préchauffer le four à 180°C."))
        order += 1
        steps.append(RecipeStep(order=order, description="Préparer la garniture (fruits, sucre, épaississant)."))
        order += 1
        steps.append(RecipeStep(order=order, description="Garnir la pâte et cuire 30–40 min selon four."))
        return steps

    if "gratin" in name or "gratin" in category:
        steps.append(RecipeStep(order=order, description="Préchauffer le four à 180°C et beurrer un plat."))
        order += 1
        steps.append(RecipeStep(order=order, description="Trancher les pommes de terre, monter en couches avec crème et fromage."))
        order += 1
        steps.append(RecipeStep(order=order, description="Cuire 40–50 min jusqu'à ce que le gratin soit doré."))
        return steps

    if "poulet" in name or "rôti" in name or "rot" in name:
        steps.append(RecipeStep(order=order, description="Préchauffer le four à 200°C."))
        order += 1
        steps.append(RecipeStep(order=order, description="Assaisonner et, si souhaité, faire mariner 30 min le poulet avec huile, ail et herbes."))
        order += 1
        steps.append(RecipeStep(order=order, description="Saisir le poulet 4–6 min de chaque côté dans une poêle chaude."))
        order += 1
        steps.append(RecipeStep(order=order, description="Terminer la cuisson au four 30–45 min selon la taille; vérifier la cuisson à cœur (≥75°C)."))
        order += 1
        steps.append(RecipeStep(order=order, description="Laisser reposer 10 min avant de découper et servir."))
        return steps

    if "poisson" in name:
        steps.append(RecipeStep(order=order, description="Préchauffer le four à 180°C."))
        order += 1
        steps.append(RecipeStep(order=order, description="Assaisonner le poisson et disposer sur une plaque huilée."))
        order += 1
        steps.append(RecipeStep(order=order, description="Cuire au four 10–20 min selon l'épaisseur (12 min pour 2 cm d'épaisseur)."))
        order += 1
        steps.append(RecipeStep(order=order, description="Vérifier l'opacité et la floculation; servir immédiatement."))
        return steps

    # plat générique
    steps.append(RecipeStep(order=order, description="Préparer et assaisonner les ingrédients principaux."))
    order += 1
    steps.append(RecipeStep(order=order, description="Cuire selon la technique adaptée (sauter, rôtir, braiser)."))
    order += 1
    steps.append(RecipeStep(order=order, description="Vérifier la cuisson et rectifier l'assaisonnement."))
    order += 1
    steps.append(RecipeStep(order=order, description="Laisser reposer 5 min puis servir."))
    return steps


def _equipment_for_category(template_name: str, category: str) -> list[str]:
    name = template_name.lower()
    if "velout" in name or "soupe" in name:
        return ["casserole", "mixeur plongeant", "planche à découper"]
    if "salade" in name:
        return ["saladier", "casserole (pour quinoa)", "planche à découper"]
    if "tarte" in name or "gratin" in name:
        return ["four", "plat à four", "rouleau à pâtisserie (optionnel)"]
    if category == "dessert":
        return ["four", "moule à tarte/plat", "fouet", "saladier"]
    if "poisson" in name or "poulet" in name:
        return ["poêle", "plaque de four", "couteau"]
    return ["poêle", "casserole", "planche à découper"]


def _times_for_difficulty(difficulty: str, category: str) -> tuple[int, int]:
    diff = difficulty.lower() if difficulty else "moyen"
    if diff == "facile":
        prep = 15
        cook = 20 if category != "dessert" else 25
    elif diff == "moyen":
        prep = 20
        cook = 30
    else:
        prep = 30
        cook = 45
    # adjust for soups and gratins
    if category == "entree" and "velout" in diff:
        cook += 10
    return prep, cook


def _build_variants(template: dict, recipe: Recipe, request: UserRequest) -> list[RecipeVariant]:
    variants: list[RecipeVariant] = []
    ingredients_lower = {i.name.lower() for i in recipe.ingredients}

    # végétarien / vegan
    if any(m in ingredients_lower for m in ("poulet", "poisson", "viande")):
        if "végétarien" in request.dietary_constraints or "vegetarian" in request.dietary_constraints:
            veg_ing = [ing for ing in ingredients_lower if ing not in ("poulet", "poisson", "viande")]
            variants.append(
                RecipeVariant(
                    type="végétarien",
                    description="Remplacer la protéine animale par du tofu, tempeh ou légumineuses selon préférence.",
                    adapted_ingredients=list(veg_ing)[:3] + ["tofu/pois chiches"],
                )
            )
        if "vegan" in request.dietary_constraints:
            non_vegan = [ing for ing in ingredients_lower if ing in ("lait", "fromage", "oeuf")]
            variants.append(
                RecipeVariant(
                    type="vegan",
                    description="Remplacer produits laitiers par alternatives végétales et protéines par tofu/légumineuses.",
                    adapted_ingredients=["lait végétal", "tofu", "huile d'olive"],
                )
            )

    # halal
    if "halal" in request.dietary_constraints:
        if any(m in ingredients_lower for m in ("poulet", "viande")):
            variants.append(
                RecipeVariant(
                    type="halal",
                    description="Utiliser viande/poulet certifiée halal ou remplacer par une option végétarienne.",
                    adapted_ingredients=["poulet halal"],
                )
            )

    # sans gluten
    if "sans gluten" in request.dietary_constraints or "gluten-free" in request.dietary_constraints:
        # detect pâte / farine
        if any("pâte" in i.name or "pate" in i.name or "farine" in i.name for i in recipe.ingredients):
            variants.append(
                RecipeVariant(
                    type="sans gluten",
                    description="Remplacer la pâte/farine par une version sans gluten (pâte GF, farine de riz).",
                    adapted_ingredients=["pâte sans gluten", "farine de riz"],
                )
            )

    return variants


def _build_description(template: dict, recipe: Recipe) -> str:
    name = template.get("name", recipe.name if recipe else "").capitalize()
    cat = template.get("category", "")
    if "tarte" in name.lower() or cat == "dessert":
        return f"{name} simple et familiale, à base de fruits et d'une pâte croustillante. Idéale en fin de repas."
    if "velout" in name.lower() or "soupe" in name.lower() or cat == "entree":
        return f"{name} onctueux et réconfortant, préparé au bouillon et mixé pour une texture lisse. Servir chaud."
    if "poulet" in name.lower() or "poisson" in name.lower() or cat == "plat":
        return f"{name} savoureux, mettant en avant une protéine rôtie ou poêlée accompagnée de légumes de saison."
    return f"{name} recette simple et goûteuse, adaptée au repas familial."


def _additional_steps_for_category(category: str, template_name: str) -> list[RecipeStep]:
    steps: list[RecipeStep] = []
    base = 1
    if category == "dessert":
        steps.append(RecipeStep(order=base, description="Préchauffer le four à 180°C."))
        base += 1
        steps.append(RecipeStep(order=base, description="Préparer la pâte et foncer le moule."))
        base += 1
        steps.append(RecipeStep(order=base, description="Garnir avec les fruits et saupoudrer de sucre si besoin."))
        base += 1
        steps.append(RecipeStep(order=base, description="Cuire 30–40 min selon le four, vérifier la cuisson à la pointe d'un couteau."))
        return steps

    if category == "entree":
        steps.append(RecipeStep(order=base, description="Faire revenir les aromatiques (oignon, ail) 4–6 min à feu moyen."))
        base += 1
        steps.append(RecipeStep(order=base, description="Ajouter les légumes et le bouillon, porter à ébullition puis laisser mijoter 15–20 min."))
        base += 1
        steps.append(RecipeStep(order=base, description="Mixer au mixeur plongeant jusqu'à obtenir la texture désirée; rectifier l'assaisonnement."))
        base += 1
        steps.append(RecipeStep(order=base, description="Servir chaud, éventuellement avec une cuillère de crème ou d'huile d'olive."))
        return steps

    # plat principal
    steps.append(RecipeStep(order=base, description="Assaisonner la protéine et saisir 3–5 min de chaque côté à feu vif."))
    base += 1
    steps.append(RecipeStep(order=base, description="Rôtir ou terminer la cuisson au four à 180–200°C selon la taille, 25–45 min."))
    base += 1
    steps.append(RecipeStep(order=base, description="Cuire les légumes d'accompagnement (rôtis ou sautés) 20–35 min."))
    base += 1
    steps.append(RecipeStep(order=base, description="Vérifier la cuisson à coeur et laisser reposer 5–10 min avant de couper et servir."))
    return steps


def _ensure_min_ingredients(ingredients: list[Ingredient], category: str) -> list[Ingredient]:
    # Ensure at least 4 ingredients by adding sensible staples
    names = {i.name.lower() for i in ingredients}
    additions = []
    if len(ingredients) >= 4:
        return ingredients
    if category == "dessert":
        candidates = [("farine de blé T55", "100", "g"), ("oeuf", "2", "unité(s)"), ("sucre", "50", "g"), ("beurre", "50", "g")]
    elif category == "entree":
        candidates = [("bouillon", "500", "ml"), ("sel", "1", "c.à.c"), ("poivre", "1", "c.à.c"), ("huile d'olive", "2", "c.à.s")]
    else:
        candidates = [("sel", "1", "c.à.c"), ("poivre", "1", "c.à.c"), ("huile d'olive", "2", "c.à.s"), ("citron", "1", "unité")]

    for name, qty, unit in candidates:
        if len(ingredients) + len(additions) >= 4:
            break
        if name.lower() not in names:
            additions.append(Ingredient(name=name, quantity=qty, unit=unit))

    return ingredients + additions


def _capitalize_first(text: str) -> str:
    if not text:
        return text
    return text[0].upper() + text[1:]


# Build a set of all known ingredient names from templates to help detect mentions
ALL_KNOWN_INGREDIENTS = set()
for t in TEMPLATES:
    for ing in t.get("ingredients", []):
        ALL_KNOWN_INGREDIENTS.add(ing.lower())


def _ensure_ingredients_mentioned_in_steps(ingredients: list[Ingredient], steps: list[RecipeStep], request: UserRequest) -> list[Ingredient]:
    names = {i.name.lower(): i for i in ingredients}
    for s in steps:
        text = s.description.lower()
        for known in ALL_KNOWN_INGREDIENTS:
            if known in text and known not in names:
                qty_per_guest, unit = _estimate_quantity_per_guest(known)
                total_qty = str(int(qty_per_guest * max(1, request.guests)))
                new_ing = Ingredient(name=known, quantity=total_qty, unit=unit)
                ingredients.append(new_ing)
                names[known] = new_ing
    return ingredients


def _ensure_category_requirements(template: dict, recipe: Recipe, request: UserRequest) -> None:
    name = (template.get("name", recipe.name) or "").lower()
    ing_names = {i.name.lower() for i in recipe.ingredients}
    # Tarte: ensure pastry or flour/eggs/butter
    if "tarte" in name:
        if not any(x in ing_names for x in ("pâte", "pate", "farine", "pâte prête", "pâte prête à l'emploi", "pâte brisée")):
            # prefer ready-made pastry
            recipe.ingredients.append(Ingredient(name="pâte prête à l'emploi", quantity="1", unit="unité"))
    # Soupe/velouté: ensure bouillon and vegetables
    if "soupe" in name or "velout" in name:
        if not any("bouillon" in x or "eau" in x for x in ing_names):
            recipe.ingredients.append(Ingredient(name="bouillon", quantity="500", unit="ml"))
        veg_keywords = ("carotte", "courgette", "oignon", "poireau", "tomate", "pommes de terre", "pomme de terre")
        if not any(k in ing_names for k in veg_keywords):
            recipe.ingredients.append(Ingredient(name="légumes variés (carotte, oignon)", quantity=str(300 * max(1, request.guests)), unit="g"))
    # Meat dish: ensure meat explicitly present
    if template.get("category") == "plat":
        if any(k in name for k in ("poulet", "bœuf", "boeuf", "porc", "agneau", "viande")) and not any(m in ing_names for m in ("poulet", "viande", "poisson", "boeuf", "porc", "agneau")):
            recipe.ingredients.append(Ingredient(name="poulet", quantity=str(400 * max(1, request.guests)), unit="g"))


GENERIC_PHRASES = [
    "préparer les ingrédients principaux",
    "préparer les ingrédients",
    "terminer et servir",
    "préparer",
    "préparer et servir",
    "vérifier la cuisson et servir chaud",
]


def _is_generic_step(text: str) -> bool:
    tl = text.lower()
    for g in GENERIC_PHRASES:
        if g in tl:
            return True
    return False


def _make_steps_precise(steps: list[RecipeStep], ingredients: list[Ingredient], template: dict) -> list[RecipeStep]:
    # Replace generic steps with more concrete instructions using ingredient names
    ing_names = [i.name for i in ingredients]
    protein = None
    for p in ("poulet", "poisson", "viande", "boeuf", "porc", "agneau", "tofu"):
        for i in ing_names:
            if p in i.lower():
                protein = i
                break
        if protein:
            break

    new_steps: list[RecipeStep] = []
    order = 1
    for s in steps:
        if _is_generic_step(s.description):
            # create concrete replacements
            # 1) prep vegetables
            vegs = [i for i in ing_names if any(k in i.lower() for k in ("carotte","courgette","oignon","poireau","poivron","tomate","aubergine","légume","légumes"))]
            if vegs:
                new_steps.append(RecipeStep(order=order, description=f"Éplucher et couper {', '.join(vegs)} en morceaux réguliers (environ 1–2 cm)."))
                order += 1
            # 2) prepare protein
            if protein:
                new_steps.append(RecipeStep(order=order, description=f"Assaisonner la {protein} avec sel et poivre, puis saisir à feu vif 3–5 min de chaque côté."))
                order += 1
                # cooking finish depending on template
                if "rôti" in (template.get("name", "").lower()):
                    new_steps.append(RecipeStep(order=order, description="Terminer la cuisson au four préchauffé à 180–200°C jusqu'à cuisson à cœur (temps selon poids)."))
                    order += 1
                else:
                    new_steps.append(RecipeStep(order=order, description="Poursuivre la cuisson à feu moyen jusqu'à cuisson complète, vérifier la cuisson à cœur."))
                    order += 1
            # 3) finish vegetables/accompaniment
            if vegs:
                new_steps.append(RecipeStep(order=order, description="Sauter les légumes 5–10 min à feu moyen jusqu'à tendreté."))
                order += 1
        else:
            new_steps.append(RecipeStep(order=order, description=s.description))
            order += 1

    # ensure at least 4 steps
    if len(new_steps) < 4:
        last_order = new_steps[-1].order if new_steps else 0
        while len(new_steps) < 4:
            last_order += 1
            new_steps.append(RecipeStep(order=last_order, description="Vérifier la cuisson et rectifier l'assaisonnement si nécessaire."))
    return new_steps


def _build_advice(template: dict, recipe: Recipe) -> str:
    name = (template.get("name", recipe.name) or "").lower()
    if "tarte" in name:
        return "Conseil : pour une pâte croustillante, réfrigérez la pâte 30 minutes avant cuisson et piquez le fond avec une fourchette."
    if "soupe" in name or "velout" in name:
        return "Conseil : mixez par petites quantités et passez au tamis pour un velouté lisse. Ajustez l'assaisonnement à la fin."
    if any(k in name for k in ("poulet","rôti","poisson","viande")):
        return "Conseil : laissez reposer la viande 8–10 minutes après cuisson pour conserver les jus."
    return "Conseil : assaisonnez progressivement et goûtez en cours de cuisson."


def _estimate_nutrition(template: dict, recipe: Recipe) -> tuple[int, int, int, int]:
    # Simple heuristic estimates per portion
    name = (template.get("name", recipe.name) or "").lower()
    ing_names = {i.name.lower() for i in recipe.ingredients}
    # Defaults for light dishes
    if "tarte" in name or template.get("category") == "dessert":
        return 350, 4, 45, 15
    if "soupe" in name or "velout" in name or template.get("category") == "entree":
        return 180, 6, 25, 5
    # Protein-rich main
    if any(k in name for k in ("poulet", "poisson", "boeuf", "boeuf", "porc", "agneau", "viande")) or any(k in ing_names for k in ("poulet", "poisson", "viande", "boeuf", "porc", "agneau")):
        return 500, 35, 30, 20
    # Fallback moderate
    return 300, 10, 35, 10


class RecipeAgent:
    """Génère des recettes plus réalistes à partir de templates simples."""

    def generate_recipes(self, menu: MenuProposal, request: UserRequest) -> list[RecipePackage]:
        packages: list[RecipePackage] = []

        for item in menu.menu_items:
            template = _choose_template_for(item.name, item.category)

            if template:
                ingredients: list[Ingredient] = []
                for ing_name in template.get("ingredients", []):
                    qty_per_guest, unit = _estimate_quantity_per_guest(ing_name)
                    total_qty = qty_per_guest * max(1, request.guests)
                    # format quantity (integer)
                    quantity = str(int(total_qty))
                    ingredients.append(
                        Ingredient(
                            name=ing_name,
                            quantity=quantity,
                            unit=unit,
                        )
                    )

                # ensure at least 4 ingredients
                ingredients = _ensure_min_ingredients(ingredients, template.get("category", item.category))

                difficulty = template.get("difficulty", "moyen")
                prep_time, cook_time = _times_for_difficulty(difficulty, template.get("category", item.category))
                tname = template.get("name", "").lower()
                # overrides for specific dishes
                if "tarte" in tname or template.get("category") == "dessert":
                    prep_time, cook_time = 15, 35
                if "velout" in tname or "soupe" in tname:
                    prep_time, cook_time = 15, 20
                if "poulet" in tname or "rôti" in tname or "roti" in tname:
                    prep_time, cook_time = max(prep_time, 20), max(cook_time, 45)
                steps = _steps_for_template(template.get("name", item.name), template.get("category", item.category))
                # ensure at least 4 steps with concrete instructions
                if len(steps) < 4:
                    # compute next order start
                    last_order = steps[-1].order if steps else 0
                    extra = _additional_steps_for_category(template.get("category", item.category), template.get("name", item.name))
                    existing_descs = {st.description.lower() for st in steps}
                    for s in extra:
                        if s.description.lower() in existing_descs:
                            continue
                        last_order += 1
                        steps.append(RecipeStep(order=last_order, description=s.description))
                        existing_descs.add(s.description.lower())
                        if len(steps) >= 4:
                            break
                equipment = _equipment_for_category(template.get("name", item.name), template.get("category", item.category))

                # build description
                description = _build_description(template, None)

                recipe = Recipe(
                    name=template.get("name", item.name),
                    category=template.get("category", item.category),
                    description=description,
                    image_url=_image_for_recipe(template.get("name", item.name)),
                    ingredients=ingredients,
                    steps=steps,
                    prep_time_minutes=prep_time,
                    cook_time_minutes=cook_time,
                    equipment=equipment,
                    difficulty=difficulty,
                    variants=[],
                )

                # Professional-level enrichments and validations
                # Portions
                recipe.portions = max(1, request.guests)
                # total time
                recipe.total_time_minutes = int(recipe.prep_time_minutes + recipe.cook_time_minutes)
                # beginner friendliness heuristic
                try:
                    diff = (recipe.difficulty or "moyen").lower()
                except Exception:
                    diff = "moyen"
                recipe.beginner_friendly = True if diff == "facile" or (len(recipe.steps) <= 6 and recipe.prep_time_minutes <= 20) else False
                # Ensure ingredients mentioned in steps exist in ingredient list
                recipe.ingredients = _ensure_ingredients_mentioned_in_steps(recipe.ingredients, recipe.steps, request)
                # Ensure category-specific requirements (tarte, soupe, viande)
                _ensure_category_requirements(template, recipe, request)
                # Make generic steps precise
                recipe.steps = _make_steps_precise(recipe.steps, recipe.ingredients, template)
                # Build a concise advice
                recipe.advice = _build_advice(template, recipe)
                # Estimate nutrition per portion
                cal, prot, carbs, fats = _estimate_nutrition(template, recipe)
                recipe.calories_kcal = cal
                recipe.proteins_g = prot
                recipe.carbs_g = carbs
                recipe.lipids_g = fats

                # build variants (guarantee at least one detailed variant)
                recipe.variants = _build_variants(template, recipe, request)
                if not recipe.variants:
                    # fallback variant depending on category/protein
                    ingr_lower = {i.name.lower(): i for i in recipe.ingredients}
                    if "poulet" in ingr_lower or "viande" in ingr_lower or "poisson" in ingr_lower:
                        # estimate replacement quantity
                        qty = 0
                        for key in ("poulet", "viande", "poisson"):
                            if key in ingr_lower:
                                try:
                                    qty = int(ingr_lower[key].quantity)
                                except Exception:
                                    qty = 400
                                break
                        tofu_qty = int(max(200, qty))
                        recipe.variants.append(
                            RecipeVariant(
                                type="végétarien",
                                description=f"Remplacer la protéine animale par {tofu_qty} g de tofu mariné.",
                                adapted_ingredients=[f"tofu ({tofu_qty} g)"],
                            )
                        )
                    elif template.get("category") == "dessert":
                        recipe.variants.append(
                            RecipeVariant(
                                type="vegan",
                                description="Remplacer le lait et le beurre par des alternatives végétales (lait végétal, margarine).",
                                adapted_ingredients=["lait végétal 200 ml", "margarine 50 g"],
                            )
                        )
                    else:
                        recipe.variants.append(
                            RecipeVariant(
                                type="alternative",
                                description="Version alternative : ajuster protéines ou remplacer par légumineuses/tofu selon préférence.",
                                adapted_ingredients=["tofu 200 g", "pois chiches 200 g"],
                            )
                        )

                # Verify coherence and normalize capitalization for description, steps, equipment and variants
                recipe.description = _capitalize_first(recipe.description or "")
                for st in recipe.steps:
                    st.description = _capitalize_first(st.description or "")
                recipe.equipment = [ _capitalize_first(e) for e in recipe.equipment ]
                for v in recipe.variants:
                    v.description = _capitalize_first(v.description or "")

                packages.append(RecipePackage(menu_item_name=item.name, recipe=recipe, alternatives=[]))
            else:
                # fallback: produce a minimal but structured recipe
                desc = f"{item.name} recette simple et adaptable."
                ingredients = [
                    Ingredient(name="ingrédient principal", quantity="400", unit="g"),
                    Ingredient(name="sel", quantity="1", unit="c.à.c"),
                    Ingredient(name="poivre", quantity="1", unit="c.à.c"),
                    Ingredient(name="huile d'olive", quantity="2", unit="c.à.s"),
                ]
                steps = _additional_steps_for_category(item.category, item.name)
                # ensure 4 steps
                if len(steps) < 4:
                    last = steps[-1].order if steps else 0
                    while len(steps) < 4:
                        last += 1
                        steps.append(RecipeStep(order=last, description="Vérifier la cuisson et servir chaud."))

                equipment = ["casserole", "poêle", "planche à découper"]
                recipe = Recipe(
                    name=item.name,
                    category=item.category,
                    description=desc,
                    image_url=_image_for_recipe(item.name),
                    ingredients=ingredients,
                    steps=steps,
                    prep_time_minutes=20,
                    cook_time_minutes=25,
                    equipment=equipment,
                    difficulty="moyen",
                )
                # ensure at least one variant
                recipe.variants = [
                    RecipeVariant(
                        type="alternative",
                        description="Version alternative : remplacer l'ingrédient principal par 400 g de tofu mariné.",
                        adapted_ingredients=["tofu 400 g"],
                    )
                ]
                # Normalize capitalization
                recipe.description = _capitalize_first(recipe.description or "")
                for st in recipe.steps:
                    st.description = _capitalize_first(st.description or "")
                recipe.equipment = [ _capitalize_first(e) for e in recipe.equipment ]
                for v in recipe.variants:
                    v.description = _capitalize_first(v.description or "")

                packages.append(RecipePackage(menu_item_name=item.name, recipe=recipe, alternatives=[]))

        return packages
