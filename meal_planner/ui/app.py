import streamlit as st

from meal_planner.agents.orchestrator import OrchestratorAgent


st.set_page_config(page_title="Meal Planner", page_icon="🍽️", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #ffffff;
        --panel: #f9fafb;
        --border: rgba(0, 0, 0, 0.1);
        --text: #1a202c;
        --muted: #718096;
        --green: #22c55e;
        --amber: #f59e0b;
        --red: #ef4444;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #ffffff 0%, #f3f4f6 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .hero {
        background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1), rgba(34,197,94,0.1));
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.25rem;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(2rem, 4vw, 3rem);
        letter-spacing: -0.04em;
        color: var(--text);
    }

    .hero p {
        color: var(--muted);
        margin-top: 0.5rem;
        margin-bottom: 0;
        font-size: 1rem;
    }

    .card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        height: 100%;
    }

    .metric-box {
        background: linear-gradient(180deg, #f9fafb, #f3f4f6);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        min-height: 120px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.4rem;
        color: var(--text);
    }

    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 14px;
        padding: 0.8rem 1rem;
    }

    .warning-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 14px;
        padding: 0.8rem 1rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 1.25rem 0 0.8rem 0;
        color: var(--text);
    }

    .budget-shell {
        background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(6,182,212,0.08));
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        min-height: 170px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.35rem 0.8rem;
        font-weight: 700;
        font-size: 0.76rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .status-ok {
        background: rgba(34, 197, 94, 0.15);
        color: #15803d;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .status-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #b45309;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .status-danger {
        background: rgba(239, 68, 68, 0.15);
        color: #991b1b;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .shopping-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0.7rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        background: rgba(59, 130, 246, 0.04);
        border-radius: 8px;
        margin-bottom: 0.4rem;
        color: var(--text);
    }

    .shopping-row:last-child {
        border-bottom: none;
    }

    .small-tag {
        display: inline-block;
        font-size: 0.72rem;
        color: var(--muted);
        background: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 999px;
        padding: 0.25rem 0.55rem;
        margin-right: 0.35rem;
    }

    .ingredient-item {
        background: white;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.55rem;
    }

    .recipe-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1rem;
        height: 100%;
    }

    .recipe-card h4 {
        margin-top: 0;
        color: var(--text);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Meal Planner</h1>
        <p>Créez un menu intelligent, cohérent et optimisé budget avec un planning réaliste.</p>
    </div>
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
    budget_ok = plan.shopping.budget_ok
    remaining = plan.shopping.budget_remaining_eur
    used_pct = plan.shopping.budget_used_pct
    avg_price = total / len(plan.shopping.items) if plan.shopping.items else 0
    
    # Calcul du budget disponible
    budget_disponible = total + remaining
    
    # Status
    status_icon = "🟢" if budget_ok else "🔴"
    status_label = "Budget respecté" if budget_ok else "Budget dépassé"
    
    # Créer une layout en colonnes : image à gauche, infos à droite
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        # Image à gauche
        st.image(
            "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=500&q=80",
            width="stretch",
            caption="Votre panier"
        )
    
    with col_right:
        # Badge statut premium
        badge_bg = "#dcfce7" if budget_ok else "#fee2e2"
        badge_border = "#22c55e" if budget_ok else "#ef4444"
        badge_text = "#15803d" if budget_ok else "#991b1b"
        
        st.markdown(f"""
        <div style="
            background: {badge_bg};
            border: 2px solid {badge_border};
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            text-align: center;
        ">
            <span style="color: {badge_text}; font-weight: 700; font-size: 1.1rem;">
                {status_icon} {status_label}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Métriques principales en 2 colonnes
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric(
                "💰 Budget Disponible",
                f"{budget_disponible:.2f} €",
                delta=None
            )
        
        with metric_col2:
            delta_value = f"{remaining:.2f} €"
            st.metric(
                "📊 Restant",
                "",
                delta=delta_value,
                delta_color="inverse" if remaining < 0 else "normal"
            )
        
        # Barre de progression premium
        st.markdown("### 📈 Utilisation du Budget")
        
        # Couleur de la barre basée sur usage
        if used_pct <= 50:
            progress_color = "#22c55e"  # Vert
        elif used_pct <= 75:
            progress_color = "#fbbf24"  # Jaune
        else:
            progress_color = "#ef4444"  # Rouge
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        ">
            <div style="flex: 1; background: #e5e7eb; border-radius: 999px; height: 12px; overflow: hidden;">
                <div style="
                    background: {progress_color};
                    width: {min(used_pct, 100)}%;
                    height: 100%;
                    border-radius: 999px;
                    transition: width 0.3s ease;
                "></div>
            </div>
            <span style="
                font-size: 1.3rem;
                font-weight: 900;
                color: {progress_color};
                min-width: 70px;
                text-align: right;
            ">{used_pct:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Infos détaillées
        budget_col1, budget_col2 = st.columns(2)
        with budget_col1:
            st.markdown(f"""
            <div style="
                background: #f8fafc;
                border-left: 4px solid #3b82f6;
                padding: 0.75rem 1rem;
                border-radius: 6px;
            ">
                <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; font-weight: 600;">Total</div>
                <div style="font-size: 1.5rem; font-weight: 900; color: #1e293b;">{total:.2f} €</div>
            </div>
            """, unsafe_allow_html=True)
        
        with budget_col2:
            remaining_color = "#ef4444" if remaining < 0 else "#22c55e"
            st.markdown(f"""
            <div style="
                background: #f8fafc;
                border-left: 4px solid {remaining_color};
                padding: 0.75rem 1rem;
                border-radius: 6px;
            ">
                <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; font-weight: 600;">Restant</div>
                <div style="font-size: 1.5rem; font-weight: 900; color: {remaining_color};">{remaining:+.2f} €</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistiques en cartes
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.markdown(
            f"""
            <div style="
                border: 1.5px solid #e2e8f0; 
                border-radius: 14px; 
                padding: 1.25rem; 
                background: linear-gradient(135deg, rgba(249,250,251,0.8) 0%, rgba(255,255,255,0.5) 100%);
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            ">
                <div style="font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 0.6rem;">💰 Coût Moyen</div>
                <div style="font-size: 2rem; font-weight: 900; color: #3b82f6;">{avg_price:.2f} €</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with stats_col2:
        st.markdown(
            f"""
            <div style="
                border: 1.5px solid #d1d5db; 
                border-radius: 14px; 
                padding: 1.25rem; 
                background: linear-gradient(135deg, rgba(240,253,250,0.8) 0%, rgba(255,255,255,0.5) 100%);
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            ">
                <div style="font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 0.6rem;">🟢 Article Moins Cher</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #22c55e;">{plan.shopping.product_least_expensive}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with stats_col3:
        st.markdown(
            f"""
            <div style="
                border: 1.5px solid #fecaca; 
                border-radius: 14px; 
                padding: 1.25rem; 
                background: linear-gradient(135deg, rgba(254,242,242,0.8) 0%, rgba(255,255,255,0.5) 100%);
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            ">
                <div style="font-size: 0.75rem; color: #718096; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 0.6rem;">🔴 Article Plus Cher</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #ef4444;">{plan.shopping.product_most_expensive}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Calcul du score budget (0-100)
    if budget_ok:
        if used_pct <= 50:
            budget_score = 95
            score_level = "🟢 Excellent"
        elif used_pct <= 75:
            budget_score = 82
            score_level = "🟢 Bon"
        else:
            budget_score = 68
            score_level = "🟠 Moyen"
    else:
        budget_score = 35
        score_level = "🔴 À optimiser"
    
    # Détails du panier avec emojis
    shopping_items_md = ""
    emoji_map = {
        "carotte": "🥕", "courgette": "🥒", "oignon": "🧅", "pomme": "🍎",
        "tomate": "🍅", "poivron": "🫑", "aubergine": "🍆", "laitue": "🥬",
        "riz": "🍚", "poulet": "🍗", "poisson": "🐟", "fromage": "🧀",
        "yaourt": "🥛", "pain": "🍞", "oeuf": "🥚", "lentille": "🫘",
        "pois": "🫛", "huile": "🫗",
    }
    
    for idx, item in enumerate(plan.shopping.items[:10], 1):
        ingredient_lower = item.ingredient.lower()
        emoji = next((emoji_map[k] for k in emoji_map if k in ingredient_lower), "🛒")
        shopping_items_md += f"\n{emoji} {item.ingredient}\nQuantité : {item.quantity} {item.unit or ''}\nPrix : {item.estimated_price_eur:.2f} €\n"
    
    if len(plan.shopping.items) > 10:
        shopping_items_md += f"\n... et {len(plan.shopping.items) - 10} articles supplémentaires"
    
    # Recommandations (basées sur les alternatives)
    recommendations = ""
    alternatives = getattr(plan.shopping, 'recommended_alternatives', [])
    if alternatives:
        recommendations = "\n" + "\n".join(f"✅ {alt}" for alt in alternatives[:3])
    
    # Conclusion
    if budget_ok:
        conclusion = f"""
🎉 Félicitations !

Votre panier respecte votre budget.

Vous disposez encore de {remaining:.2f} € pour vos prochains achats."""
    else:
        conclusion = f"""
🚨 Attention

Votre panier dépasse le budget de {abs(remaining):.2f} €.

L'application des optimisations proposées permettrait de réduire ce dépassement."""
    
    # Affichage du contenu formaté en Markdown simple
    st.markdown("""
    # 🛒 SHOPPING BUDGET DÉTAILLÉ
    
    ## 📊 RÉSUMÉ BUDGÉTAIRE
    """)
    
    # Cartes d'infos en colonnes
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("💰 Budget disponible", f"{budget_disponible:.2f} €")
        st.metric("💵 Budget restant", f"{remaining:+.2f} €")
    with res_col2:
        st.metric("🛍️ Dépenses estimées", f"{total:.2f} €")
        st.metric("📦 Articles", len(plan.shopping.items))
    
    # Badge statut
    badge_text = f"✅ Budget respecté" if budget_ok else f"🚨 Budget dépassé"
    st.info(f"### {status_icon} {badge_text}")
    
    st.markdown("---")
    
    st.markdown(f"""
    ## 🏆 SCORE BUDGET
    
    ### {budget_score} / 100  ({score_level})
    """)
    
    st.markdown("---")
    
    st.markdown(f"""
    ## 🛒 VOTRE PANIER
    {shopping_items_md}
    """)
    
    st.markdown("---")
    
    st.markdown(f"""
    ## 📌 ANALYSE RAPIDE
    
    - **🏆 Produit le plus cher :** {plan.shopping.product_most_expensive}
    - **💚 Produit le moins cher :** {plan.shopping.product_least_expensive}
    - **📊 Coût moyen par article :** {avg_price:.2f} €
    """)
    
    st.markdown("---")
    
    st.markdown(f"""
    ## 🚀 RECOMMANDATIONS INTELLIGENTES
    {recommendations}
    """)
    
    st.markdown("---")
    
    st.markdown(f"""
    ## 🎯 CONCLUSION
    {conclusion}
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 💰 ÉCONOMISEZ IMMÉDIATEMENT
    
    ✅ **Remplacer le produit le plus coûteux** par une alternative équivalente
    
    🌱 **Acheter les légumes de saison** actuellement disponibles
    
    🏷️ **Sélectionner les marques distributeur** lorsque disponible
    
    🏪 **Vérifier les promotions** des enseignes voisines
    
    ---
    
    📉 **Gain potentiel estimé:** Entre 8 € et 12 € d'économies
    """)

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
