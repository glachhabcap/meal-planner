# Fiche de mission par agent

## 1. Objectif général

Ce projet est construit pour apprendre le développement logiciel à travers une architecture simple : chaque agent a une mission claire, un contrat d'entrée et de sortie, et une responsabilité de validation.

Chaque personne peut se positionner sur un agent et développer :
- la logique métier ;
- la structure des données attendues ;
- les tests de validation ;
- la documentation de son rôle ;
- l'amélioration du comportement du système global.

Le principe fondamental est simple :
- l'Orchestrator pilote le flux ;
- chaque agent est spécialisé ;
- l'agent ne doit pas faire le travail des autres agents ;
- chaque sortie doit être testable et cohérente.

---

## 2. Pourquoi développer un agent séparément ?

Parce que cela permet de travailler proprement et pédagogiquement.

Chaque agent apporte une valeur métier différente :
- le Menu Agent décide du repas ;
- le Recipe Agent détaille les recettes ;
- le Shopping Budget Agent vérifie le coût ;
- l'Organization Agent organise la préparation ;
- l'Orchestrator Agent valide la cohérence globale.

Cette séparation donne plusieurs avantages :
- plus de clarté ;
- moins de dépendances entremêlées ;
- plus facile à tester ;
- plus facile à corriger ;
- plus facile à expliquer à d'autres personnes.

---

## 3. Règle de base pour chaque agent

Avant de coder, chaque agent doit répondre à 4 questions :

1. Quel est mon objectif exact ?
2. Quelles sont mes entrées ?
3. Quelles sont mes sorties attendues ?
4. Qu'est-ce qui doit être validé dans les tests ?

Un agent ne doit jamais :
- refaire le travail d'un autre agent ;
- manipuler des structures non définies ;
- dépendre de valeurs hardcodées sans logique ;
- sortir un résultat sans test de cohérence.

---

## 4. Mission de l'Orchestrator Agent

### Rôle
L'Orchestrator Agent est le chef d'orchestre du système.

### Objectif
- analyser la demande utilisateur ;
- extraire les contraintes ;
- appeler les bons agents dans le bon ordre ;
- vérifier la cohérence globale ;
- décider si un recalcul est nécessaire ;
- produire le plan final.

### Étapes de développement

1. Lire la demande utilisateur en texte brut.
2. Transformer la demande en objet `UserRequest`.
3. Identifier les contraintes importantes :
   - nombre de personnes ;
   - budget ;
   - temps maximum ;
   - contraintes alimentaires ;
   - préférences de saison ;
   - occasion spéciale.
4. Appeler le Menu Agent.
5. Appeler le Recipe Agent.
6. Appeler le Shopping Budget Agent.
7. Appeler l'Organization Agent.
8. Vérifier la cohérence globale.
9. Construire le `FinalMealPlan`.
10. Si le budget ou le planning ne sont pas satisfaisants, relancer un recalcul.

### Challenge minimum
Créer une logique qui détecte au moins :
- un budget trop élevé ;
- un temps de préparation trop long ;
- une recette non compatible avec les contraintes alimentaires.

### Pourquoi tester ?
Parce que l'orchestrateur est le point de décision global. Si ce point est faux, tout le système semble correct alors qu'il ne l'est pas.

### Comment tester ?
Écrire des tests qui vérifient :
- une demande standard produit un plan final ;
- un budget dépassé déclenche un recalcul ou un warning ;
- un planning trop long est signalé ;
- les sorties sont cohérentes entre les différents agents.

### Exemple de test
- demander 8 personnes avec un budget 30€ ;
- vérifier qu'un warning est généré ;
- vérifier que le plan final contient des avertissements explicites.

---

## 5. Mission du Menu Agent

### Rôle
Le Menu Agent produit le menu proposé au client.

### Objectif
- proposer un menu cohérent ;
- tenir compte des contraintes ;
- garantir un bon équilibre entre entrée, plat, accompagnement, dessert ;
- rester compatible avec le budget et le temps.

### Étapes de développement

1. Recevoir `UserRequest`.
2. Identifier les points de contrainte.
3. Choisir un menu structuré en plusieurs catégories.
4. Ajouter une justification pour chaque choix.
5. Produire un `MenuProposal` de qualité.
6. Vérifier que le menu respecte les préférences et la saison.

### Challenge minimum
Le menu doit faire au moins :
- une entrée ;
- un plat ;
- un accompagnement ;
- un dessert ;
- une justification claire par élément.

### Pourquoi tester ?
Parce qu'un mauvais menu peut rendre l'ensemble du plan incohérent, même si les autres agents sont corrects.

### Comment tester ?
Écrire des tests qui vérifient :
- que le menu contient les catégories attendues ;
- que le menu ne contient pas d’éléments contradictoires ;
- que les régimes alimentaires sont bien pris en compte ;
- que le menu est cohérent avec le budget et le nombre de convives.

### Exemple de test
- demander un menu pour 6 personnes avec 60€ et 90 minutes ;
- vérifier qu’il existe au moins 4 éléments ;
- vérifier qu’un choix végétarien ou halal est bien présent si demandé.

---

## 6. Mission du Recipe Agent

### Rôle
Le Recipe Agent crée les recettes associées au menu.

### Objectif
- générer des recettes détaillées ;
- proposer des ingrédients, quantités et étapes ;
- intégrer les variantes alimentaires ;
- compatibilité avec les besoins du client.

### Étapes de développement

1. Recevoir le menu et la demande utilisateur.
2. Pour chaque item du menu, créer une recette.
3. Définir les ingrédients et les quantités.
4. Décrire les étapes de préparation.
5. Ajouter temps de préparation et cuisson.
6. Ajouter le matériel nécessaire.
7. Ajouter des variantes pertinentes.
8. Vérifier la cohérence avec le menu.

### Challenge minimum
Le recipe agent doit produire :
- au moins une recette complète par élément du menu ;
- un `prep_time_minutes` ;
- un `cook_time_minutes` ;
- au moins une variante ;
- une description claire de la recette.

### Pourquoi tester ?
Parce qu’une recette mal définie entraîne ensuite des erreurs sur le budget, le planning et la faisabilité.

### Comment tester ?
Écrire des tests qui vérifient :
- le nombre de recettes correspond au nombre d’éléments du menu ;
- chaque recette a un nom, des ingrédients et des étapes ;
- les variantes existent pour les contraintes alimentaires ;
- les temps ne sont pas absurdes.

### Exemple de test
- demander un menu avec un régime végétarien ;
- vérifier qu’au moins une recette a une variante végétarienne ;
- vérifier que les temps sont cohérents.

---

## 7. Mission du Shopping Budget Agent

### Rôle
Le Shopping Budget Agent calcule les achats et le coût estimé.

### Objectif
- regrouper les ingrédients ;
- calculer le coût total ;
- comparer au budget cible ;
- proposer des alternatives si nécessaire.

### Étapes de développement

1. Recevoir les recettes générées.
2. Extraire les ingrédients et leurs quantités.
3. Regrouper les ingrédients similaires.
4. Attribuer un prix estimé à chaque produit.
5. Calculer le total.
6. Comparer le total au budget.
7. Produire des alternatives économiques.
8. Retourner un `ShoppingResult` clair.

### Challenge minimum
Le shopping agent doit :
- calculer un total estimé ;
- indiquer si le budget est respecté ;
- produire une liste de courses ;
- proposer au moins une alternative économique.

### Pourquoi tester ?
Parce qu’un budget faux casse confiance dans le système. Un mauvais calcul est souvent visible immédiatement pour l’utilisateur.

### Comment tester ?
Écrire des tests qui vérifient :
- le total est bien calculé ;
- le budget est validé ou non ;
- la liste de courses contient des éléments utiles ;
- les alternatives sont pertinentes.

### Exemple de test
- budget cible 60€ ;
- total estimé 80€ ;
- vérifier que `budget_ok` est `False` ;
- vérifier qu’au moins une alternative est proposée.

---

## 8. Mission de l'Organization Agent

### Rôle
L'Organization Agent construit le planning de préparation.

### Objectif
- organiser les étapes ;
- tenir compte du temps disponible ;
- repérer les tâches dépendantes ;
- proposer un planning réaliste ;
- signaler si la préparation est trop longue.

### Étapes de développement

1. Recevoir les recettes et la demande.
2. Déterminer les principales étapes de préparation.
3. Définir les dépendances entre tâches.
4. Estimer une durée pour chaque étape.
5. Calculer la durée totale.
6. Vérifier si le temps est respecté.
7. Produire le `PlanningResult`.

### Challenge minimum
L’organization agent doit :
- produire un planning avec au moins 3 étapes ;
- calculer la durée totale ;
- indiquer si le planning est réaliste ;
- fournir des commentaires utiles.

### Pourquoi tester ?
Parce que l’utilisateur veut un plan utilisable, pas seulement une liste de textes.

### Comment tester ?
Écrire des tests qui vérifient :
- la somme des étapes est cohérente ;
- la durée totale est calculée correctement ;
- le planning est signalé comme réaliste ou non ;
- les dépendances sont bien respectées.

### Exemple de test
- demander 90 minutes max ;
- vérifier que le planning total est inférieur ou égal à cette limite ;
- sinon, vérifier que le système émet un warning.

---

## 9. Pourquoi et comment tester chaque agent ?

### Pourquoi tester ?
Parce qu’un agent sans test est un agent non fiable.

Les tests servent à :
- valider le comportement réel ;
- éviter les régressions ;
- vérifier que les contraintes sont prises en compte ;
- rassurer l’équipe sur la qualité du travail ;
- montrer que le code ne “fonctionne pas par chance”.

### Comment tester ?
Avec Pytest, de manière simple et directe.

Règles :
- écrire les tests avant ou en même temps que le développement ;
- tester les vrais comportements, pas des hypothèses ;
- utiliser des objets réels ;
- garder les tests lisibles ;
- tester les cas positifs et négatifs.

### Bon pattern de test

```python
def test_menu_agent_returns_valid_menu():
    request = UserRequest(
        raw_text="6 personnes, budget 60€, 90 minutes",
        guests=6,
        budget_eur=60,
        max_prep_minutes=90,
        dietary_constraints=[],
    )

    menu = MenuAgent().generate_menu(request)

    assert menu is not None
    assert len(menu.menu_items) >= 4
    assert any(item.category == "plat" for item in menu.menu_items)
```

### Les 3 types de tests à privilégier

1. Test de structure :
   - les objets sont bien créés ;
   - les champs attendus existent.

2. Test de logique :
   - le budget est bien calculé ;
   - le planning respecte le temps.

3. Test de validation :
   - le système détecte les incohérences ;
   - les warnings sont bien produits.

---

## 10. Niveau de challenge minimum

Chaque agent doit avoir au moins :

- une logique métier non vide ;
- une sortie structurée (Pydantic) ;
- 2 ou 3 tests utiles ;
- un cas limite ;
- un cas “normal” ;
- un cas “problème”.

Cela permet d’apprendre sans tomber dans un projet trop complexe dès le départ.

---

## 11. Niveau de challenge à viser ensuite

Quand la base est validée, on peut ajouter :
- gestion de demandes plus complexes ;
- contraintes combinées ;
- alternatives plus nombreuses ;
- budget optimisé ;
- recettes plus détaillées ;
- planning avec parallélisation ;
- perception plus intelligente du contexte.

---

## 12. Exemple de répartition possible

### Agent 1 : Menu Agent
- développer le menu ;
- tests sur les catégories ;
- validation des règles de cohérence.

### Agent 2 : Recipe Agent
- développer les recettes ;
- tests sur les variantes ;
- validation des ingrédients et temps.

### Agent 3 : Shopping Budget Agent
- développer le calcul de prix ;
- tests sur le total et les alternatives.

### Agent 4 : Organization Agent
- développer le planning ;
- tests sur le temps et les dépendances.

### Agent 5 : Orchestrator Agent
- développer la chaîne complète ;
- tests sur la validation et les recalculs.

---

## 13. Règle finale

Le but n'est pas d'avoir un agent “parfait” dès le départ.

Le but est de développer un agent qui :
- a une responsabilité claire ;
- produit une sortie exploitable ;
- est vérifiable ;
- peut être amélioré ensuite sans casser le système.

C’est cette logique qui rend le projet solide, pédagogique et évolutif.

---

# Fiche de mission par participant

## Participant 1 — Orchestrator Agent

### Mission
Piloter le flux complet du projet et garantir la cohérence du résultat final.

### Livrables attendus
- analyse de la demande utilisateur ;
- extraction des contraintes ;
- appel des agents dans le bon ordre ;
- validation globale ;
- génération du `FinalMealPlan`.

### Plan de développement
1. Lire le code de l'orchestrateur existant.
2. Définir les contraintes que le système doit détecter.
3. Créer des tests sur des demandes standards et atypiques.
4. Ajouter la logique de validation globale.
5. Ajouter les warnings et les recalculs si le budget ou le planning dépasse la limite.

### Challenge minimum
- détecter au moins 3 problèmes possibles : budget trop élevé, temps trop long, incompatibilité de contraintes.

### Critères de réussite
- la demande est bien transformée en `UserRequest` ;
- les agents sont appelés dans le bon ordre ;
- les warnings sont explicites ;
- le résultat final est cohérent.

---

## Participant 2 — Menu Agent

### Mission
Proposer un menu cohérent en fonction de la demande utilisateur.

### Livrables attendus
- menu structuré (entrée, plat, accompagnement, dessert) ;
- explication de chaque choix ;
- prise en compte des contraintes de budget, de saison et de régime.

### Plan de développement
1. Comprendre le `MenuProposal` et `MenuItem`.
2. Créer un menu simple avec logique métier.
3. Ajouter les justifications de chaque choix.
4. Vérifier les cas de contraintes alimentaires et saisonnières.
5. Ajouter des tests unitaires sur les catégories et la cohérence du menu.

### Challenge minimum
- le menu doit toujours contenir au moins 4 éléments ;
- les contraintes doivent être visibles dans le choix.

### Critères de réussite
- le menu est cohérent ;
- les choix sont justifiés ;
- les régimes demandés sont respectés.

---

## Participant 3 — Recipe Agent

### Mission
Produire les recettes associées au menu avec variantes et temps de préparation réalistes.

### Livrables attendus
- recette par item du menu ;
- ingrédients ;
- étapes ;
- temps de préparation et cuisson ;
- variantes adaptées.

### Plan de développement
1. Lire le modèle `Recipe`, `RecipePackage` et `RecipeVariant`.
2. Générer une recette complète pour chaque élément du menu.
3. Ajouter les variations halal, végétariennes, sans gluten ou substitutions utiles.
4. Vérifier les temps de préparation.
5. Mettre en place des tests sur les recettes et sur les variantes.

### Challenge minimum
- chaque recette doit avoir ingrédients, étapes, temps et au moins une variante.

### Critères de réussite
- les recettes sont complètes ;
- les variantes sont cohérentes ;
- les temps ne sont pas absurdes ;
- les recettes restent adaptées à la demande.

---

## Participant 4 — Shopping Budget Agent

### Mission
Estimer le coût total, construire la liste de courses et vérifier le budget.

### Livrables attendus
- liste de courses ;
- prix estimés ;
- total calculé ;
- budget validé ou non ;
- alternatives économiques.

### Plan de développement
1. Comprendre `ShoppingItem` et `ShoppingResult`.
2. Extraire les ingrédients des recettes.
3. Regrouper les éléments similaires.
4. Calculer le total estimé.
5. Ajouter le test du budget.
6. Proposer au moins une alternative sensible.

### Challenge minimum
- calculer correctement le total ;
- savoir dire si le budget est respecté ;
- proposer une alternative claire.

### Critères de réussite
- le total est cohérent ;
- le budget est correctement validé ;
- la liste de courses est exploitable ;
- l’alternative économique est utile.

---

## Participant 5 — Organization Agent

### Mission
Construire un planning réaliste de préparation et de service.

### Livrables attendus
- étapes de préparation ;
- dépendances entre tâches ;
- durée totale ;
- commentaire sur la faisabilité ;
- validation de la limite de temps.

### Plan de développement
1. Comprendre `PlanningStep` et `PlanningResult`.
2. Structurer les étapes clés du repas.
3. Ajouter les dépendances de tâches.
4. Calculer le temps total.
5. Vérifier que le planning tient dans le temps demandé.
6. Ajouter des tests sur la durée et la logique de dépendance.

### Challenge minimum
- produire un planning avec au moins 3 étapes ;
- calculer la durée totale ;
- signaler si le plan dépasse la limite.

### Critères de réussite
- le planning est lisible ;
- le temps total est cohérent ;
- les dépendances sont respectées ;
- le message de validation est clair.

---

## 6. Plan de développement commun à tous les participants

### Étape 1 — Comprendre le contrat
- lire les modèles Pydantic concernés ;
- lire le code de l’agent ;
- comprendre les entrées et sorties.

### Étape 2 — Implémenter la logique
- écrire la fonctionnalité principale ;
- garder le code simple et lisible ;
- éviter les valeurs en dur si la logique peut être calculée.

### Étape 3 — Tester le comportement
- écrire un test normal ;
- écrire un test limite ;
- écrire un test d’erreur ou de warning.

### Étape 4 — Intégrer au système
- vérifier que l’agent fonctionne dans l’orchestrateur ;
- regarder si les résultats sont cohérents avec les autres agents.

### Étape 5 — Valider le projet
- lancer `pytest` ;
- vérifier qu’aucun test n’est cassé ;
- vérifier que le résultat final reste lisible.

---

## 7. Règle de qualité pour tous

Chaque participant doit livrer :
- code propre ;
- tests associés ;
- sortie structurée ;
- logique explicite ;
- documentation minimaliste du rôle.

L’objectif n’est pas d’être le plus rapide, mais d’être cohérent, compréhensible et testable.

---

## 8. Exemple de répartition pour un atelier de 5 personnes

- Personne 1 : Orchestrator Agent
- Personne 2 : Menu Agent
- Personne 3 : Recipe Agent
- Personne 4 : Shopping Budget Agent
- Personne 5 : Organization Agent

Chaque personne travaille sur sa mission avec ses tests, puis tout le monde valide l’intégration finale.

---

## 9. Résultat attendu

À la fin du projet, chaque participant doit pouvoir répondre à ces trois questions :

1. Quelle est ma mission ?
2. Quelles sont mes entrées et sorties ?
3. Comment je sais que mon agent fonctionne correctement ?

C’est ce qui permet d’apprendre le développement logiciel de manière sérieuse et concrète.
