# Workflow Git et GitHub

## 1. À quoi sert Git ?

Git est un outil qui permet de suivre les changements dans un projet.

Il garde un historique de ce qui a été modifié, quand, et par qui.

Pour un projet comme Meal Planner, Git permet de :
- enregistrer les avancées du projet ;
- revenir en arrière si nécessaire ;
- travailler en équipe sans écraser le travail des autres ;
- organiser le développement par petits morceaux.

## 2. À quoi sert GitHub ?

GitHub est une plateforme en ligne qui héberge des projets Git.

Il sert à :
- partager le code avec l'équipe ;
- centraliser le projet ;
- proposer des modifications via des Pull Requests ;
- collaborer à distance ;
- garder une trace de l’évolution du projet.

## 3. Les concepts de base

### Le dépôt (repository)

Le dépôt est le dossier du projet. C'est l'endroit où tout est stocké.

### La branche

Une branche est une version de travail séparée du projet principal.

Exemple :
- main : version principale stable ;
- feature/menu-agent : travail sur l'agent menu ;
- fix/budget-check : correction d'un point de logique.

Les branches permettent de travailler sans casser le projet principal.

### Le commit

Un commit est une sauvegarde logique d'un ensemble de changements.

Un bon commit :
- est petit ;
- a un message clair ;
- couvre un seul objectif.

Exemple de message de commit :

```bash
git commit -m "Ajout du Menu Agent et des tests associés"
```

### La Pull Request (PR)

Une Pull Request est une demande pour fusionner une branche dans une autre.

Elle sert à :
- montrer ce qui a été modifié ;
- demander une revue ;
- valider la cohérence avant de fusionner.

## 4. Le workflow conseillé pour le projet

Le projet est pensé pour une équipe de débutants. Le workflow le plus simple est le suivant :

1. Cloner le dépôt.
2. Créer une branche dédiée.
3. Travailler sur une petite partie du projet.
4. Faire des commits réguliers.
5. Lancer les tests.
6. Ouvrir une Pull Request.
7. Demander une revue.
8. Fusionner si tout est cohérent.

## 5. Commandes utiles

### Cloner le projet

```bash
git clone <url-du-repo>
```

### Vérifier l'état

```bash
git status
```

### Créer une branche

```bash
git checkout -b feature/menu-agent
```

ou plus moderne :

```bash
git switch -c feature/menu-agent
```

### Ajouter des fichiers

```bash
git add .
```

### Faire un commit

```bash
git commit -m "Ajout du Menu Agent"
```

### Envoyer la branche vers GitHub

```bash
git push origin feature/menu-agent
```

### Ouvrir une Pull Request

Sur GitHub :
- aller dans l'onglet "Pull requests" ;
- cliquer sur "New pull request" ;
- choisir la branche source et la branche cible ;
- rédiger une description claire ;
- demander une revue.

## 6. Pourquoi utiliser des branches ?

Les branches évitent les erreurs de travail simultané.

Sans branches, plusieurs personnes peuvent écraser ou modifier le même fichier au même moment.

Avec des branches :
- tout le monde travaille sur son propre espace ;
- les modifications sont plus faciles à relire ;
- les erreurs sont plus faciles à corriger.

## 7. Pourquoi faire des commits réguliers ?

Parce qu'un bon historique aide à :
- comprendre les évolutions du projet ;
- reprendre une version antérieure ;
- expliquer clairement ce qui a été fait ;
- faciliter la coévolution du travail de groupe.

## 8. Ce qu'il faut retenir comme débutant

Ne pas avoir peur de Git.

Git n'est pas là pour compliquer le projet. Il sert à sécuriser le travail.

Les bonnes habitudes de débutant sont :
- travailler sur une branche ;
- faire des petits commits ;
- vérifier les changements avant de les valider ;
- demander une revue avant de fusionner ;
- ne pas avoir peur de revenir en arrière.

## 9. GitHub et le travail collaboratif

GitHub transforme le code en un espace de travail partagé.

Il permet de :
- partager le projet ;
- centraliser la version de référence ;
- discuter des changements ;
- suivre les tâches ;
- examiner les améliorations.

Dans ce projet, GitHub a aussi une valeur pédagogique : il permet de voir comment un groupe travaille ensemble dans les mêmes outils.

## 10. Conseils pratiques

- Faites des changements petits et compréhensibles.
- Donnez des messages de commit clairs.
- Vérifiez votre travail avant d'ouvrir une PR.
- Ne gardez pas une branche trop longtemps sans la fusionner.
- Si vous êtes perdu, demandez à l'équipe ou à Copilot de vous expliquer le contexte.

## 11. En résumé

Git et GitHub ne sont pas des outils réservés aux experts.

Ils sont simplement des outils pour :
- enregistrer le travail ;
- partager le travail ;
- protéger la qualité ;
- collaborer sans confusion.

Dans le cadre du projet Meal Planner, ils sont une partie essentielle de la pédagogie.
