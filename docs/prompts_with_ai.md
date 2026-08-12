# Prompts IA pour les agents

## 1. Pourquoi ce document existe ?

Dans ce projet, les agents ne sont pas des personnes. Ce sont des modules spécialisés qui ont chacun une mission claire.

L'IA est utilisée pour aider à :
- expliquer un comportement ;
- produire un squelette de code ;
- proposer des tests ;
- suggérer des améliorations ;
- challenger une logique.

Le point important est le suivant :

L'IA est un assistant, pas une autorité.

Elle aide à réfléchir, mais la décision finale revient à l'équipe.

## 2. Les agents du projet

Chaque agent a un rôle spécifique :
- Orchestrator Agent : contrôle le flux global ;
- Menu Agent : construit le menu ;
- Recipe Agent : crée les recettes et variantes ;
- Shopping Budget Agent : calcule le budget ;
- Organization Agent : construit le planning.

## 3. Comment utiliser les prompts IA de manière utile

Les meilleurs prompts sont :
- courts ;
- précis ;
- centrés sur le besoin ;
- orientés vers le contexte réel du projet.

### Bon exemple

```text
Explique-moi le rôle du Menu Agent dans ce projet en français simple.
```

### Bon exemple

```text
Propose-moi 3 tests pour vérifier qu'un menu respecte les contraintes alimentaires.
```

### Bon exemple

```text
Le Recipe Agent doit produire des variantes pertinentes. Quelles variantes sont vraiment utiles pour un repas avec un végétarien et un client halal ?
```

### Bon exemple

```text
Explique-moi pourquoi le Shopping Budget Agent doit être séparé du Recipe Agent.
```

## 4. Exemples de prompts utiles pour chaque agent

### Pour l'Orchestrator Agent

```text
Explique-moi le rôle de l'Orchestrator Agent dans le flux général du projet.
```

```text
Que doit faire l'orchestrateur si le budget dépasse le plafond ?
```

```text
Propose-moi une vérification simple pour contrôler la cohérence du projet final.
```

### Pour le Menu Agent

```text
Quel est le bon comportement attendu du Menu Agent pour une demande avec 8 personnes et un budget serré ?
```

```text
Propose-moi un menu cohérent pour une soirée avec 6 personnes, budget de 60€ et 1h30 de préparation.
```

```text
Quels cas limites dois-je tester pour le Menu Agent ?
```

### Pour le Recipe Agent

```text
Quel est le objectif du Recipe Agent dans ce projet ?
```

```text
Propose-moi des variantes pour une recette qui doit être compatible avec un végétarien et une personne halal.
```

```text
Quelles recettes sont peu pertinentes à proposer dans ce contexte ?
```

### Pour le Shopping Budget Agent

```text
Explique-moi comment calculer un budget estimé à partir des ingrédients d'une recette.
```

```text
Quelles alternatives économiques pourrait-on proposer si le budget est trop élevé ?
```

```text
Propose-moi des tests pour vérifier qu'un budget est bien détecté comme dépassé.
```

### Pour l'Organization Agent

```text
Quel est le rôle de l'Organization Agent ?
```

```text
Comment organiser un planning réaliste pour 6 personnes avec 1h30 de préparation ?
```

```text
Quels éléments doivent être détectés comme parallélisables ?
```

## 5. Bonnes pratiques pour interroger l'IA

### 1. Donnez le contexte

Exemple :

```text
Je travaille sur le Menu Agent d'un projet Meal Planner. Le but est de proposer un menu pour 6 personnes, budget 60€, contraintes halal et végétarienne.
```

### 2. Demandez une explication, pas seulement un résultat

Exemple :

```text
Explique-moi pourquoi cette règle de menu est utile.
```

### 3. Demandez des tests

Exemple :

```text
Propose-moi des cas limites pour tester ce comportement.
```

### 4. Demandez des améliorations

Exemple :

```text
Comment rendre ce comportement plus simple, plus lisible et plus facile à tester ?
```

### 5. Demandez à challenger la logique

Exemple :

```text
Qu'est-ce qui pourrait aller mal si le budget est dépassé ?
```

## 6. Ce qu'il ne faut pas faire

Évitez de donner à Copilot une consigne trop vague comme :

```text
Fais le projet.
```

Le résultat sera souvent trop large, trop peu précis, ou pas adapté au contexte.

Il vaut mieux demander :

```text
Explique-moi le rôle de l'Orchestrator Agent et donne-moi les tests à écrire pour vérifier son comportement.
```

## 7. Comment challenger les résultats de l'IA

L'IA peut proposer une réponse très convaincante, mais elle peut quand même être fausse, incomplète ou trop optimiste.

Il faut toujours vérifier :
- si la demande a bien été comprise ;
- si les contraintes sont respectées ;
- si les résultats sont cohérents ;
- s'il existe des cas limites oubliés ;
- s'il manque une règle métier importante.

### Checklist rapide

- La réponse correspond-elle à la demande ?
- Les contraintes sont-elles toutes respectées ?
- Y a-t-il des cas de bord ?
- La logique est-elle plausible ?
- Le résultat est-il testable ?
- Le code est-il lisible ?

## 8. Exemples de prompts de revue critique

```text
Je pense que ce menu dépasse le budget. Peux-tu le relire et me dire où il y a un risque ?
```

```text
Cette recette semble compatible, mais qu'est-ce qu'on peut oublier dans les variantes ?
```

```text
Peux-tu me proposer des scénarios de test qui pourraient casser la logique du planning ?
```

```text
Quel est le point le plus fragile dans ce code ?
```

## 9. Les meilleurs usages de Copilot dans ce projet

Copilot est particulièrement utile pour :
- expliquer les fichiers ;
- générer le squelette d'un agent ;
- proposer une première version de test ;
- suggérer des cas limites ;
- reformuler des exigences ;
- clarifier une logique confuse.

Copilot n'est pas là pour remplacer la réflexion, mais pour la soutenir.

## 10. En résumé

Dans ce projet, les prompts IA doivent être :
- simples ;
- précis ;
- centrés sur une responsabilité claire ;
- suivis d'une validation critique.

Le bon usage de Copilot dans un contexte de formation n'est pas :
"demander une solution complète sans vérifier".

Le bon usage est :
"demander une aide, comprendre, tester, challenger, corriger".

C'est cela qui fait la vraie valeur de l'outil.
