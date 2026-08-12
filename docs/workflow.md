# Workflow du projet

1. La demande utilisateur est saisie.
2. L'orchestrateur transforme la demande en UserRequest.
3. Le Menu Agent propose un menu.
4. Le Recipe Agent produit les recettes.
5. Le Shopping Budget Agent calcule le coût.
6. L'Organization Agent établi le planning.
7. L'orchestrateur vérifie la cohérence globale.
8. Le résultat final est affiché dans l'interface Streamlit.

## Boucle de correction

Si le budget ou le planning est incohérent :
- l'orchestrateur relance le flux ;
- le nombre d'itérations est limité.
