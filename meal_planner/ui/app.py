import streamlit as st

from meal_planner.agents.orchestrator import OrchestratorAgent


st.set_page_config(page_title="Meal Planner", page_icon="🍽️")
st.title("Meal Planner")
st.caption("Projet pédagogique sur les agents IA et le développement Python")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stVerticalBlock"] > div:has(> div) {
        border-radius: 12px;
        padding: 0.8rem 1rem;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

user_text = st.text_area(
    "Décrivez votre repas :",
    value=(
        "Je reçois 6 personnes samedi soir. Budget 60€. "
        "Maximum 1h30 de préparation. Une personne est végétarienne, "
        "une autre mange halal. Je souhaite privilégier les légumes de saison."
    ),
    height=180,
)

if st.button("Générer le plan de repas", use_container_width=True):
    plan = OrchestratorAgent().run(user_text)

    st.subheader("📌 Résumé global")
    st.success(plan.final_summary)

    if plan.warnings:
        with st.container():
            st.warning("Avertissements")
            for warning in plan.warnings:
                st.write(f"- {warning}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nombre de personnes", plan.menu.menu_items[0].description and "6")
    with col2:
        st.metric("Budget estimé", f"{plan.shopping.total_estimated_eur:.2f} €")
    with col3:
        st.metric("Temps total", f"{plan.planning.total_duration_minutes} min")

    st.subheader("🍽️ Menu")
    for item in plan.menu.menu_items:
        with st.container():
            st.markdown(f"### {item.name} ({item.category})")
            st.write(item.description)
            st.write(f"Justification : {item.justification}")

        st.subheader("👨‍🍳 Recettes")
        for package in plan.recipes:
                recipe = package.recipe
                with st.container():
                        title = recipe.name[0].upper() + recipe.name[1:] if recipe.name else recipe.name
                        cat = recipe.category[0].upper() + recipe.category[1:] if recipe.category else recipe.category
                        prep = getattr(recipe, "prep_time_minutes", "--")
                        cook = getattr(recipe, "cook_time_minutes", "--")
                        total = getattr(recipe, "total_time_minutes", "--")
                        diff = getattr(recipe, "difficulty", "--")
                        beginner = getattr(recipe, "beginner_friendly", False)

                        # Build compact HTML for uniform presentation
                        html = f"""
<div style="margin-bottom:8px">
    <h3 style="margin:0 0 4px 0">{title} ({cat})</h3>
</div>
<div style="margin-bottom:6px">
    <strong>Description :</strong>
    <div style="margin-left:1rem; margin-top:4px;">{recipe.description or ''}</div>
</div>
<div style="margin-bottom:6px">
    <strong>Informations :</strong>
    <div style="margin-left:1rem; margin-top:4px;">
        <ul style="margin:0; padding-left:1rem;">
            <li>Préparation : {prep} min</li>
            <li>Cuisson : {cook} min</li>
            <li>Temps total : {total} min</li>
            <li>Difficulté : {str(diff).capitalize()}</li>
            <li>Portions : {getattr(recipe, 'portions', '--')}</li>
            <li>Adapté aux débutants : {'Oui' if beginner else 'Non'}</li>
        </ul>
    </div>
</div>
"""

                        # Ustensiles
                        if recipe.equipment:
                                items = ''.join([f"<li>{e}</li>" for e in recipe.equipment])
                                html += f"""
<div style="margin-bottom:6px"> 
    <strong>Ustensiles :</strong>
    <div style="margin-left:1rem; margin-top:4px;">
        <ul style="margin:0; padding-left:1rem;">{items}</ul>
    </div>
</div>
"""

                        # Ingredients
                        if recipe.ingredients:
                                items = ''.join([f"<li>{ing.name} : {ing.quantity} {ing.unit or ''}</li>" for ing in recipe.ingredients])
                                html += f"""
<div style="margin-bottom:6px">
    <strong>Ingrédients :</strong>
    <div style="margin-left:1rem; margin-top:4px;">
        <ul style="margin:0; padding-left:1rem;">{items}</ul>
    </div>
</div>
"""

                        # Steps (ordered)
                        if recipe.steps:
                                steps = ''.join([f"<li>{step.description}</li>" for step in recipe.steps])
                                html += f"""
<div style="margin-bottom:6px">
    <strong>Étapes :</strong>
    <div style="margin-left:1rem; margin-top:4px;">
        <ol style="margin:0; padding-left:1.2rem;">{steps}</ol>
    </div>
</div>
"""

                        # Variants (clean duplicate prefixes)
                        if recipe.variants:
                                items_list = []
                                for v in recipe.variants:
                                        desc = v.description or ""
                                        label = (v.type or "").capitalize()
                                        low = desc.lower()
                                        # remove leading occurrences like 'version alternative:' or the label itself
                                        if low.startswith("version alternative") or low.startswith("version"):
                                                parts = desc.split(":", 1)
                                                if len(parts) > 1:
                                                        desc = parts[1].strip()
                                        elif low.startswith(label.lower()):
                                                parts = desc.split(":", 1)
                                                if len(parts) > 1:
                                                        desc = parts[1].strip()
                                        items_list.append(f"<li>{label} : {desc}</li>")
                                items = ''.join(items_list)
                                html += f"""
<div style="margin-bottom:6px">
    <strong>Variantes :</strong>
    <div style="margin-left:1rem; margin-top:4px;">
        <ul style="margin:0; padding-left:1rem;">{items}</ul>
    </div>
</div>
"""

                        # Advice
                        if getattr(recipe, "advice", None):
                                advice = recipe.advice
                                if advice.lower().startswith("conseil"):
                                        parts = advice.split(":", 1)
                                        if len(parts) > 1:
                                                advice = parts[1].strip()
                                        else:
                                                advice = advice[len("conseil"):].strip(" :")
                                html += f"""
<div style="margin-bottom:6px">
    <strong>Conseil de préparation :</strong>
    <div style="margin-left:1rem; margin-top:4px;">{advice}</div>
</div>
"""

                        # Nutrition
                        if getattr(recipe, "calories_kcal", None) is not None:
                                html += f"""
<div style="margin-bottom:6px">
    <strong>Valeurs nutritionnelles :</strong>
    <div style="margin-left:1rem; margin-top:4px;">
        <ul style="margin:0; padding-left:1rem;">
            <li>Calories : {recipe.calories_kcal} kcal</li>
            <li>Protéines : {recipe.proteins_g} g</li>
            <li>Glucides : {recipe.carbs_g} g</li>
            <li>Lipides : {recipe.lipids_g} g</li>
        </ul>
    </div>
</div>
"""

                        st.markdown(html, unsafe_allow_html=True)

    st.subheader("🛒 Courses et budget")
    total = plan.shopping.total_estimated_eur
    st.write(f"Total estimé : {total:.2f} €")
    st.write(f"Budget respecté : {'Oui' if plan.shopping.budget_ok else 'Non'}")
    for item in plan.shopping.items:
        st.write(f"- {item.ingredient} : {item.quantity} {item.unit or ''} — {item.estimated_price_eur:.2f} €")
    if plan.shopping.recommended_alternatives:
        st.write("Alternatives recommandées :")
        for alternative in plan.shopping.recommended_alternatives:
            st.write(f"- {alternative}")

    st.subheader("⏱️ Planning")
    for step in plan.planning.schedule:
        dependencies = ", ".join(step.dependencies) if step.dependencies else "Aucune"
        st.write(f"- {step.title} : {step.start_minute} min → {step.end_minute} min | dépendances : {dependencies}")
    st.write(f"Durée totale : {plan.planning.total_duration_minutes} min")
    st.write(f"Réaliste dans la limite : {'Oui' if plan.planning.realistic_within_limit else 'Non'}")
    if plan.planning.comments:
        st.write("Commentaires :")
        for comment in plan.planning.comments:
            st.write(f"- {comment}")
