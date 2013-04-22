Projet Mangez Mieux

# Introduction

Site Web en Python/Django répondant au besoin : mangez varié et équilibré sans vous fatiguer!


# Dépendances 

* django (>= 1.4) 
* djangorestframework
* markdown
* pyyaml 
* django-filter
* python-dateutil

# Architecture : Django-app

mangezmieux/
  |- api/                               // API
  |- auth/                              // Profil utilisateur (token, gouts)
  |- commande/                          // Application de commande des produits
  |- core/                              // Module central
  |- home/                              // Application homepage (news)
  |- recette/		                    // Application "catalogue de recettes"
  |- static/                            // CSS + JS
  |- templates/                         // HTML
  |- manage.py                          // Script d'administration du projet
  |- settings.py                        // Paramètres du projet (DB, apps...)
  |- urls.py                            // fichiers de redirection des urls
scripts/
  |- data.csv		                    // Données API Openfoodfacts.org
  |- install.sh		                    // Script d'installation de la base de données 
  |- initial_data.json                  // Données de bases
  |- openfoodfacts_to_mangezmieux.pl    // Script d'import des données openfoodfacts dans MangezMieux




