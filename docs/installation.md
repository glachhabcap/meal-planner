# Guide d'installation

## 1. Objectif

Ce document explique exactement comment installer et lancer le projet Meal Planner sur votre machine.

Vous allez pouvoir :
- ouvrir le projet dans VS Code ;
- créer un environnement Python isolé ;
- installer les dépendances ;
- lancer les tests ;
- démarrer l'application Streamlit.

Ce guide est pensé pour les débutants.

---

## 2. Prérequis

Avant de commencer, vérifiez que vous avez bien :
- Git installé ;
- VS Code installé ;
- Python 3.11 ou une version plus récente ;
- le projet cloné ou téléchargé sur votre ordinateur ;
- un terminal ouvert.

---

## 3. Ouvrir le projet dans VS Code

1. Ouvrez VS Code.
2. Cliquez sur "File" > "Open Folder".
3. Sélectionnez le dossier du projet Meal Planner.
4. Ouvrez le terminal intégré de VS Code.

Le dossier racine du projet contient normalement :
- `meal_planner/`
- `docs/`
- `tests/`
- `data/`
- `README.md`
- `requirements.txt`

---

## 4. Se placer dans le bon dossier

Dans le terminal, vérifiez que vous êtes bien à la racine du projet.

```bash
pwd
ls
```

Vous devez voir le fichier `requirements.txt` et le dossier `meal_planner`.

Si ce n'est pas le bon dossier, allez-y :

```bash
cd "C:/chemin/vers/votre/projet/Project_Meal_Planner_Agents"
```

Exemple réel :

```bash
cd "C:/Users/ton_nom/OneDrive - Capgemini/Desktop/Project_Meal_Planner_Agents"
```

---

## 5. Créer un environnement virtuel

Le but d'un environnement virtuel est d'isoler les dépendances du projet.

### 5.1 Sur Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 5.2 Sur Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 5.3 Sur Git Bash / Linux / Mac

```bash
python -m venv .venv
source .venv/bin/activate
```

Quand l'environnement est activé, votre prompt de terminal doit afficher quelque chose comme :

```bash
(.venv)
```

---

## 6. Installer les dépendances

À la racine du projet, tapez :

```bash
pip install -r requirements.txt
```

Si cela ne fonctionne pas, essayez :

```bash
python -m pip install -r requirements.txt
```

Les dépendances principales sont :
- Streamlit
- Pydantic
- Pytest

---

## 7. Vérifier que tout est bien installé

```bash
python --version
pip list
```

Vous pouvez aussi vérifier que le projet est bien chargé :

```bash
pytest
```

---

## 8. Lancer les tests

Pour vérifier que le projet est cohérent :

```bash
pytest
```

Pour lancer un test précis :

```bash
pytest tests/test_menu_agent.py
```

Si vous voulez voir les détails pendant les tests :

```bash
pytest -q
```

---

## 9. Lancer l'application Streamlit

Important : il faut être dans la racine du projet et avoir activé l'environnement virtuel.

Si tu tapes `streamlit run ...` sans avoir activé le bon environnement, tu peux obtenir cette erreur :

```python
ModuleNotFoundError: No module named 'meal_planner'
```

La commande fiable dans ce projet est :

```bash
python -m streamlit run meal_planner/ui/app.py
```

Cette commande utilise bien le Python du projet et évite les conflits avec un autre Streamlit installé globalement.

Si vous avez un message d'email de Streamlit au démarrage, laissez le champ vide et validez avec Entrée.

Le navigateur s'ouvre automatiquement. Sinon, copiez l'URL affichée dans le terminal, par exemple :

```text
http://localhost:8501
```

---

## 10. Commandes complètes à copier-coller

### Windows PowerShell

```powershell
cd "C:/Users/ton_nom/OneDrive - Capgemini/Desktop/Project_Meal_Planner_Agents"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest
python -m streamlit run meal_planner/ui/app.py
```

### Git Bash / Linux / Mac

```bash
cd "/c/Users/ton_nom/OneDrive - Capgemini/Desktop/Project_Meal_Planner_Agents"
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest
python -m streamlit run meal_planner/ui/app.py
```

---

## 11. En cas de problème

Si quelque chose ne marche pas, faites dans l'ordre :

1. Vérifiez que vous êtes dans le bon dossier.
2. Vérifiez que le virtualenv est activé.
3. Vérifiez que les dépendances sont installées.
4. Relancez la commande qui a échoué.
5. Lisez le message d'erreur complet.
6. Demandez de l'aide à l'équipe ou à Copilot.

Important :
- ne pas paniquer ;
- ne pas copier des commandes sans comprendre le contexte ;
- rester calme, les erreurs Python sont normales au début.

---

## 12. Bonnes habitudes de débutant

- ouvrez toujours le terminal au bon endroit ;
- activez le bon environnement virtuel ;
- relancez les tests après chaque modification importante ;
- ne modifiez pas tout d'un coup ;
- ne prenez pas les commandes au hasard ;
- gardez le projet propre et lisible.

---

## 13. Résumé

Pour lancer le projet, la logique est simple :

1. ouvrir le projet ;
2. créer l'environnement virtuel ;
3. installer les dépendances ;
4. lancer les tests ;
5. démarrer Streamlit.

C'est la base du travail collaboratif en Python et en développement logiciel.

