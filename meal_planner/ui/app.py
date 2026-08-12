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
            st.markdown(f"### {recipe.name} ({recipe.category})")
            st.write(f"Préparation : {recipe.prep_time_minutes} min")
            st.write(f"Cuisson : {recipe.cook_time_minutes} min")
            st.write(f"Difficulté : {recipe.difficulty}")
            st.write("Ingrédients :")
            for ingredient in recipe.ingredients:
                ingredient_label = f"- {ingredient.name}: {ingredient.quantity} {ingredient.unit or ''}".strip()
                st.write(ingredient_label)
            st.write("Étapes :")
            for step in recipe.steps:
                st.write(f"{step.order}. {step.description}")
            if recipe.variants:
                st.write("Variantes :")
                for variant in recipe.variants:
                    st.write(f"- {variant.type} : {variant.description}")

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
