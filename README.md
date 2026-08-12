# Meal Planner

Le projet Meal Planner est une application pédagogique de planification de repas créée pour découvrir le développement Python, le travail collaboratif, les outils Git/GitHub, GitHub Copilot et la logique de plusieurs agents spécialisés.

## Objectif du projet

Meal Planner permet de transformer une demande utilisateur en langage naturel en un résultat exploitable :
- un menu ;
- des recettes ;
- des variantes adaptées ;
- une liste de courses ;
- un budget estimé ;
- un planning de préparation.

Le but du projet n'est pas de réaliser une application de production complète. Le but est de démontrer une architecture simple, claire et pédagogique.

## Stack utilisée

- Python
- Streamlit
- Pydantic
- Pytest

## Contraintes du projet

- pas de React ;
- pas de JavaScript frontend ;
- pas de Docker ;
- pas de base de données ;
- pas d'API externe ;
- pas de framework agent complexe.

## Architecture générale

```text
meal_planner/
├─ agents/
├─ models/
├─ data/
├─ tests/
├─ docs/
├─ wiki/
├─ ui/
├─ README.md
├─ requirements.txt
├─ pytest.ini
└─ .gitignore
```

## Agents du système

Le projet est construit autour de plusieurs agents spécialisés :

- Orchestrator Agent : contrôle le flux global ;
- Menu Agent : propose le menu ;
- Recipe Agent : crée les recettes et les variantes ;
- Shopping Budget Agent : calcule le budget et les achats ;
- Organization Agent : construit le planning de préparation.

Les agents ne communiquent pas directement entre eux. Ils utilisent des objets Python structurés via Pydantic, et l'Orchestrator centralise le flux.

## Exemple d'utilisation

Exemple de demande utilisateur :

"Je reçois 6 personnes samedi soir. Budget 60€. Maximum 1h30 de préparation. Une personne est végétarienne, une autre mange halal. Je souhaite privilégier les légumes de saison."

Le système peut produire :
- un menu cohérent ;
- des recettes correspondantes ;
- des variantes adaptées ;
- une liste de courses estimée ;
- un budget global ;
- un plan de préparation réaliste.

## Modèles principaux

Les échanges entre agents passent par des objets structurés, notamment :
- UserRequest
- MenuProposal
- Recipe
- RecipePackage
- ShoppingResult
- PlanningResult
- FinalMealPlan

## Documentation complémentaire

- [docs/git_github_workflow.md](docs/git_github_workflow.md)
- [docs/installation.md](docs/installation.md)
- [docs/prompts_with_ai.md](docs/prompts_with_ai.md)
- [docs/architecture.md](docs/architecture.md)

## Installation rapide

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
streamlit run meal_planner/ui/app.py
```

Sur Windows PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
streamlit run meal_planner/ui/app.py
```

## Objectif pédagogique

Le projet permet de découvrir :
- VS Code ;
- Git et GitHub ;
- les branches et les Pull Requests ;
- GitHub Copilot ;
- les agents IA spécialisés ;
- la validation des résultats produits par l'IA ;
- le travail collaboratif dans un projet logiciel simple.

## Contribuer au projet

Chaque participant peut travailler sur un agent ou sur un aspect du projet avec une responsabilité claire.

La méthode recommandée est :
- comprendre le rôle de son agent ;
- lire les tests associés ;
- modifier une petite partie du comportement ;
- exécuter les tests ;
- ouvrir une Pull Request.

## Rôle de la documentation

La documentation du projet sert à guider les participants sans les submerger :
- le README présente le projet ;
- les documents dans docs complètent les points techniques et méthodologiques ;
- le wiki garde des ressources utiles pour les recettes, variantes et contraintes.

## Résumé

Meal Planner est un projet pédagogique conçu pour apprendre le développement logiciel et la collaboration de manière concrète, sans complexité inutile.

- un changement dans une partie impacte les autres ;
- le système doit rester cohérent ;
- l'Orchestrateur est la personne qui veille à ce que l'ensemble tient debout.

---

# 6. Explorer le repository sans panique

Quand on ouvre le repository pour la première fois, on peut avoir l'impression de tomber dans un projet très complexe.

En réalité, il y a beaucoup de dossiers, mais ils sont organisés pour aider la compréhension.

Voici l'arborescence du projet :

```text
meal_planner/
├─ agents/
├─ models/
├─ data/
├─ tests/
├─ docs/
├─ wiki/
├─ ui/
├─ README.md
├─ requirements.txt
├─ pytest.ini
└─ .gitignore
```

## 6.1 Le dossier agents/

C'est le cœur du projet.

On y trouve les agents spécialisés :
- Menu Agent
- Recipe Agent
- Shopping Budget Agent
- Organization Agent
- Orchestrator

Chaque agent a une mission claire.

## 6.2 Le dossier models/

C'est le dossier des structures de données.

On y trouve les objets Pydantic qui représentent les entrées et sorties du système :
- UserRequest
- MenuProposal
- Recipe
- RecipePackage
- ShoppingResult
- PlanningResult
- FinalMealPlan

Ces objets servent à donner une forme claire aux échanges.

## 6.3 Le dossier data/

Il contient les données locales utilisées par les agents :
- prix des ingrédients ;
- légumes de saison ;
- modèles de recettes.

Cela permet de travailler sans base de données et sans API externe.

## 6.4 Le dossier tests/

Le dossier tests contient les vérifications du projet.

On y trouve des tests pour chacun des agents et pour l'orchestrateur.

Le but est de vérifier :
- que le comportement est bien là ;
- que les agents répondent aux besoins ;
- que les règles métier sont respectées.

## 6.5 Le dossier docs/

Le dossier docs contient la documentation de projet :
- architecture ;
- workflow ;
- règles de développement ;
- répartition des responsabilités.

## 6.6 Le dossier wiki/

Le wiki est un espace où l'on peut conserver des recettes, variantes, contraintes alimentaires et conseils réutilisables.

C'est un peu comme un carnet de cuisine partagé et versionné.

## 6.7 Le dossier ui/

Le dossier ui contient l'interface Streamlit.

C'est la partie visible pour l'utilisateur. Elle permet de saisir la demande et d'afficher les résultats.

Le message clé :

"Vous n'avez pas besoin de comprendre tous les dossiers pour contribuer."

Vous pouvez commencer par un seul agent, puis comprendre petit à petit le reste.

---

# 7. Quel est mon périmètre ?

Dans ce projet, chaque personne travaille principalement sur un seul agent.

C'est important pour la pédagogie, parce que cela évite de se perdre dans tout le système dès le départ.

Voici le périmètre typique.

## 7.1 Orchestrator Agent

Objectif :
- gérer le flux complet ;
- vérifier la cohérence globale ;
- relancer si besoin.

Fichiers importants :
- agents/orchestrator.py
- models/
- tests/test_orchestrator.py

Contributions possibles :
- améliorer la logique de validation ;
- ajouter une règle de cohérence ;
- détecter un problème de budget ou de planning ;
- améliorer le message final.

## 7.2 Menu Agent

Objectif :
- proposer un menu adapté à la demande.

Fichiers importants :
- agents/menu_agent.py
- tests/test_menu_agent.py

Contributions possibles :
- ajouter une logique plus riche pour les préférences saisonnières ;
- mieux gérer les contraintes alimentaires ;
- proposer des menus plus économiques ou plus variés.

## 7.3 Recipe Agent

Objectif :
- produire les recettes et les variantes pertinentes.

Fichiers importants :
- agents/recipe_agent.py
- tests/test_recipe_agent.py
- wiki/

Contributions possibles :
- ajouter des variantes ;
- améliorer le traitement des allergies ;
- enrichir les fiches de recettes ;
- clarifier les substitutions.

## 7.4 Shopping Budget Agent

Objectif :
- calculer les achats et le coût global.

Fichiers importants :
- agents/shopping_budget_agent.py
- tests/test_shopping_budget_agent.py
- data/ingredient_prices.csv

Contributions possibles :
- améliorer les calculs ;
- ajouter des alternatives moins chères ;
- mieux gérer les quantités ;
- corriger des estimations peu réalistes.

## 7.5 Organization Agent

Objectif :
- construire le planning et vérifier faisabilité.

Fichiers importants :
- agents/organization_agent.py
- tests/test_organization_agent.py

Contributions possibles :
- rendre le planning plus détaillé ;
- détecter les tâches parallélisables ;
- améliorer la gestion des délais ;
- vérifier la charge de travail réelle.

Le message clé :

"Vous ne devez pas tout comprendre du projet pour commencer. Il suffit de comprendre votre agent et ses tests."

---

# 8. Comment utiliser GitHub Copilot

GitHub Copilot est un assistant utile, mais il n'est pas une magie qui remplace la réflexion.

Il ne s'agit pas d'un outil qui donne automatiquement la bonne réponse. Il s'agit d'un outil qui aide à :
- expliquer du code ;
- proposer une structure ;
- générer du squelette ;
- suggérer des tests ;
- accélérer le travail.

### Vous pouvez lui demander des choses comme :
- "Explique ce fichier en français simple."
- "Quel est le rôle de cet agent ?"
- "Résume cette fonction." 
- "Propose un test pour ce comportement."
- "Quels cas limites manquent ici ?"
- "Comment améliorer cette règle ?"
- "Que risque-t-il de se passer si le budget est dépassé ?"
- "Peux-tu me proposer une version plus simple de ce code ?"
- "Montre-moi une façon de tester ce scénario."

### Exemples de prompts utiles

- "Explique-moi ce que fait ce module sans jargon technique."
- "Quel est le périmètre de cette fonction ?"
- "Peux-tu me proposer 3 tests de bord pour ce composant ?"
- "Quelles sont les erreurs possibles dans cette logique ?"
- "Comment pourrais-je rendre ce code plus lisible pour un débutant ?"

### Les erreurs fréquentes de l'IA

Copilot peut produire des réponses impressionnantes mais parfois incomplètes, incohérentes ou trop optimistes.

Voici les erreurs à surveiller :
- le code semble correct mais ne respecte pas la demande ;
- un test est proposé mais pas adapté au vrai besoin ;
- le résultat semble réaliste sans vérifier les contraintes ;
- l'IA suppose des données absentes ;
- le code est plus complexe que nécessaire ;
- la logique manque de cohérence avec les autres agents.

Le bon réflexe :

"Je ne valide pas automatiquement. Je vérifie, je questionne, je teste."

---

# 9. Méthode recommandée pour développer son agent

Voici une méthode simple, claire et rassurante.

## Étape 1 : comprendre la mission de l'agent

Avant d'écrire du code, lisez la mission du rôle.

Posez-vous cette question :
- "À quoi ce composant doit répondre ?"

## Étape 2 : lire les entrées

Quel est le type de donnée reçu par l'agent ?

Dans ce projet, les entrées sont souvent des objets Pydantic comme :
- UserRequest
- MenuProposal
- RecipePackage

## Étape 3 : lire les sorties

Quelle forme doit renvoyer l'agent ?

Exemple :
- MenuProposal
- RecipePackage
- ShoppingResult
- PlanningResult

## Étape 4 : lire les tests

Les tests sont votre meilleur point de départ.

Ils indiquent la cible de comportement sans ambiguïté.

## Étape 5 : demander des explications à Copilot

Exemple :
- "Explique-moi ce que ce test attend exactement."
- "Quelle est la différence entre ces deux objets ?"
- "Peut-tu me montrer ce qu'un bon comportement pour cet agent devrait produire ?"

## Étape 6 : modifier une petite partie

Ne cherchez pas à tout reconstruire d'un coup.

Faites un petit changement, puis vérifiez.

## Étape 7 : tester

Exécutez les tests associés à votre agent.

Le principe est simple :
- si les tests passent, on a un bon signal ;
- si les tests échouent, on corrige.

## Étape 8 : valider

Regardez le résultat avec un esprit critique.

Est-ce que la réponse est cohérente ?
Est-ce que les contraintes sont respectées ?
Est-ce que les données sont plausibles ?

## Étape 9 : faire un commit

Quand le comportement semble correct, on peut enregistrer le travail.

Un commit doit être :
- lisible ;
- explicite ;
- cohérent avec le changement apporté.

## Étape 10 : créer une Pull Request

Une Pull Request est simplement une demande de revue.

On montre ce que l'on a modifié, on explique pourquoi, et on permet à d'autres personnes de vérifier.

C'est une étape de collaboration, pas de jugement.

---

# 10. Comment un testeur doit challenger l'IA

Ce point est crucial.

L'IA est utile, mais elle n'est pas infaillible.

Un testeur ne doit pas accepter automatiquement une réponse produite par Copilot ou par un agent.

Il faut toujours se poser les bonnes questions.

## Checklist de vigilance

- Est-ce que la réponse respecte vraiment la demande ?
- Toutes les contraintes sont-elles prises en compte ?
- Y a-t-il des cas limites oubliés ?
- Les résultats sont-ils cohérents ?
- Que se passe-t-il si le budget est dépassé ?
- Que se passe-t-il si une recette n'est pas compatible avec les contraintes alimentaires ?
- Les calculs sont-ils plausibles ?
- Le planning est-il réaliste en temps ?
- Les variantes proposées sont-elles vraiment pertinentes ?
- Le menu tient-il compte de la saison et des besoins du groupe ?

### Exemples de situations à tester

- budget trop faible ;
- recette incompatible avec une allergie ;
- temps de préparation dépassé ;
- menu peu équilibré ;
- variantes trop nombreuses et non utiles ;
- résultat global cohérent mais avec un détail incohérent.

### Règle d'or :

"Ne pas croire l'IA juste parce qu'elle semble convaincante."

Un bon testeur cherche la cohérence, la logique et la robustesse.

---

# 11. Déroulement des ateliers

## Session 1 : Découverte du projet et de son environnement

Objectifs :
- ouvrir le repository ;
- comprendre la structure générale ;
- installer les outils ;
- découvrir VS Code ;
- explorer les premiers fichiers ;
- comprendre le but du projet.

À la fin de cette session, le participant doit savoir :
- ce que fait l'application ;
- où se trouvent les principaux dossiers ;
- comment le projet est organisé ;
- quel est son périmètre de travail.

## Session 2 : Développement et amélioration des agents

Objectifs :
- travailler sur son agent ;
- lire les dépendances ;
- écrire ou modifier des tests ;
- valider un petit comportement ;
- utiliser Copilot avec méthode.

À la fin de cette session, le participant doit être capable de :
- expliquer son agent ;
- identifier ses entrées et sorties ;
- écrire un test de base ;
- améliorer une règle métier.

## Session 3 : Pull Requests, revue collaborative et démonstration finale

Objectifs :
- présenter son travail ;
- ouvrir une Pull Request ;
- revoir un autre agent ;
- corriger un point de cohérence ;
- expliquer le résultat final au groupe.

À la fin de cette session, le participant doit comprendre :
- comment collaborer dans un projet partagé ;
- comment relire un travail sans s'approprier la logique d'autrui ;
- comment présenter ses changements clairement ;
- comment remettre en question les résultats avant de les livrer.

---

# 12. Questions fréquentes

## Je ne comprends pas le code. Que faire ?

Commencez par un fichier simple. Ne cherchez pas tout comprendre d'un coup.

Demandez à Copilot :
- "Explique ce fichier en français simple."
- "Quel est le but de cette fonction ?"
- "Où est-ce que cette donnée arrive ?"

Le but n'est pas d'être rapide. Le but est de comprendre.

## Puis-je demander à Copilot d'expliquer un fichier entier ?

Oui, à condition de le faire de manière raisonnable.

Exemple :
- "Explique-moi ce fichier en sections et en simple français."

Mais attention : il vaut mieux demander des explications par blocs. Un fichier entier peut être long à analyser.

## Comment savoir si j'ai cassé quelque chose ?

En lisant les tests, puis en exécutant les tests du module sur lequel vous travaillez.

Si un test échoue, cela donne un signal clair. Vous n'avez pas besoin de paniquer : c'est une étape normale.

## Dois-je comprendre toute l'application ?

Non.

Pour commencer, il suffit de comprendre :
- votre agent ;
- ce qu'il reçoit ;
- ce qu'il produit ;
- les tests associés.

Le reste viendra plus tard.

## Puis-je revenir en arrière après un commit ?

Oui. C'est le principe même de Git.

Vous pouvez toujours revenir en arrière si une modification pose problème.

## Que faire si Copilot propose quelque chose qui me semble étrange ?

Posez des questions.

Exemples :
- "Pourquoi as-tu choisi cette règle ?"
- "Quel est le risque ?"
- "Ce résultat respecte-t-il les contraintes de l'utilisateur ?"
- "Peux-tu me montrer un exemple de cas limite ?"

## Comment savoir si mon agent fonctionne correctement ?

À travers :
- les tests ;
- les cas de validation ;
- la cohérence du résultat ;
- la capacité à expliquer ce qu'il fait.

Un agent ne fonctionne pas parce qu'il "paraît intelligent". Il fonctionne parce qu'il produit des résultats cohérents et testables.

---

# Conseils pratiques pour démarrer

- Ouvrez le repository sans pression.
- Commencez par le dossier qui correspond à votre agent.
- Lisez les tests d'abord.
- Demandez à Copilot de vous expliquer les points obscurs.
- Testez souvent, mais sans peur.
- Ne prenez pas les réponses de l'IA comme vérité absolue.
- Écrivez des commentaires simples dans votre code.
- Discutez avec le groupe si un comportement semble étrange.
- Cherchez la compréhension, pas la perfection.

---

# En résumé

Meal Planner est un projet pédagogique conçu pour apprendre sans stress.

Ce n'est pas une course à la performance technique. C'est une expérience de découverte :
- du code ;
- des outils ;
- du travail en équipe ;
- de la collaboration avec l'IA ;
- de la validation critique.

Le projet montre qu'un système peut être composé de petites responsabilités, bien séparées, et qu'un bon travail de collaboration repose sur la clarté, la discipline et la curiosité.

L'important n'est pas de tout savoir dès le départ.

L'important est d'apprendre, de tester, d'expliquer, de challenger et de progresser ensemble.

Bienvenue dans cette aventure.
