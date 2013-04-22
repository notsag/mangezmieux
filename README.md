# Projet Mangez Mieux

## Introduction

Site Web en Python/Django répondant au besoin : mangez varié et équilibré sans vous fatiguer!


## Dépendances 

### Système

* python 2.7
* django (>= 1.4)
* MySQL (>=5.1)

### Python

* djangorestframework
* markdown
* pyyaml 
* django-filter
* python-dateutil

## Architecture : Django-app

* mangezmieux/
    * api/
    * auth/ _Profil utilisateur (token, gouts)_
    * commande/ _Application de commande des produits_
    * core/ _Module central_
    * home/ _Application homepage (news)_
    * recette/ _Application "catalogue de recettes"_
    * static/ _CSS + JS_
    * templates/ _HTML_
    * manage.py _Script d'administration du projet_
    * settings.py _Paramètres du projet (DB, apps...)_
    * urls.py _Fichiers de redirection des urls_
* scripts/
    * data.csv _Données API Openfoodfacts.org_
    * install.sh _Script d'installation de la base de données_
    * initial\_data.json  _Données de base_
    * openfoodfacts\_to\_mangezmieux.pl _Script d'import des données openfoodfacts dans MangezMieux_




