# Architecture du projet Meal Planner

## Objectif

Le projet simule un système multi-agents en Python. Les agents ne sont pas autonomes. Ils sont des modules spécialisés, chacun avec une responsabilité unique.

## Rôle de l'orchestrateur

L'orchestrateur central :
- reçoit la demande utilisateur ;
- extrait les contraintes ;
- appelle les agents spécialisés ;
- valide les résultats ;
- relance des agents si nécessaire ;
- assemble le résultat final.

## Rôle des agents

### Menu Agent
Produit un menu cohérent.

### Recipe Agent
Produit les recettes associées et les variantes pertinentes.

### Shopping Budget Agent
Calcule la liste de courses et le budget.

### Organization Agent
Construit le planning de préparation.

## Règles de communication

Les agents ne communiquent pas directement entre eux.
Tous les échanges passent par des objets Pydantic structurés.

## Pédagogie

L'objectif est que chaque personne travaille sur un agent distinct et comprenne à la fois :
- son rôle ;
- ses entrées / sorties ;
- les tests associés ;
- la manière dont le projet s'intègre dans l'ensemble.
