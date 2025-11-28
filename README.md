# Mini algèbre relationnelle (SPJRUD)
[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)

Auteur : Mohammed Amine KHAMLICHI  
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/

## 🎯 Résumé du projet
Moteur Python d’algèbre relationnelle SPJRUD avec mini-langage texte et chargeur de fichiers `.sqf`. Le code fournit un REPL, des exemples et une suite de tests pour valider les opérations relationnelles.

## 🧭 Contexte et objectif
Projet inspiré des travaux pratiques de Bases de Données (SPJRUD). Objectif principal : manipuler des relations en mémoire, parser des expressions SPJRUD/SQF simplifiées et exécuter un REPL pour explorer les requêtes.

## 🔑 Fonctionnalités principales
- Modèle `Relation` avec validation de schéma, suppression des doublons et affichage tabulaire.
- Opérations SPJRUD : sélection, projection, jointure naturelle, renommage, union, différence.
- Parseur d’expressions SPJRUD/SQF et chargeur de fichiers `.sqf`.
- REPL interactif : LIST, SHOW, EVAL, LOAD, HELP, QUIT.
- Jeu d’exemples et suite de tests pytest.

## 🛠️ Stack technique
- Python 3.10+
- Standard library uniquement (+ pytest pour les tests)

## ⚙️ Installation
1. Créer un environnement virtuel : `python -m venv .venv`
2. Activer l’environnement : `. .venv/Scripts/activate` (Windows) ou `source .venv/bin/activate` (macOS/Linux)
3. Installer les dépendances : `pip install -r requirements.txt`

## 🚀 Utilisation
- Lancer le REPL : `python -m minirel.repl`
- Charger un fichier `.sqf` au démarrage : `python -m minirel.repl exemples/universite.sqf`
- Exemples de commandes :
  ```
  rel> LIST
  rel> SHOW STUDENT
  rel> EVAL SELECT year >= 2 FROM STUDENT
  rel> LOAD chemin/vers/fichier.sqf
  rel> HELP
  rel> QUIT
  ```

## 🗂️ Structure du dépôt
- `minirel/relation.py` : modèle Relation et affichage
- `minirel/operations.py` : opérations SPJRUD
- `minirel/parser.py` : parseur d’expressions SPJRUD/SQF
- `minirel/sqf_loader.py` : chargeur `.sqf` simplifié
- `minirel/examples.py` : relations d’exemple
- `minirel/repl.py` : boucle interactive
- `tests/` : tests unitaires et d’intégration (dont échantillons `.sqf`)
- `sqf_exemples_20160912/` : jeux de fichiers `.sqf` utilisés pour la validation

## ✅ Tests
- Commande : `pytest`
- Intégration continue : workflow GitHub Actions `.github/workflows/ci.yml` (Python 3.10-3.12)

## 🌟 Compétences mises en avant
- Manipulation de données relationnelles et algèbre SPJRUD
- Parsing et évaluation d’expressions
- Conception de REPL et expérience CLI
- Tests automatisés avec pytest et CI GitHub Actions
