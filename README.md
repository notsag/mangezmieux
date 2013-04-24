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
* python-imaging

### Mise en prod

* apache2
* libapache2-mod-wsgi

voir la procédure de la [doc Django](https://docs.djangoproject.com/en/1.2/howto/deployment/modwsgi/).

## Architecture : Django-app

* **debian/** _Fichiers pour le packaging_
* **Makefile** _Fichier de Makefile pour le Packaging_
* **mangezmieux/**
    * **api/**
    * **auth/** _Profil utilisateur (token, gouts)_
    * **commande/** _Application de commande des produits_
    * **core/** _Module central_
    * **home/** _Application homepage (news)_
    * **initial\_data.json**  _Données de base_
    * **manage.py** _Script d'administration du projet_
    * **mysqlfulltextsearch/** _Module de recherche fulltext_
    * **panier/** _Module de gestion de panier_
    * **planning/** _Application de planning des repas_
    * **produit/** _Code relatif aux produits_
    * **recette/** _Application "catalogue de recettes"_
    * **settings.py** _Paramètres du projet (DB, apps...)_
    * **scripts/**
      * **data.csv** _Données API Openfoodfacts.org_
      * **db\_install.sh** _Script d'installation de la base de données_
      * **openfoodfacts\_to\_mangezmieux.pl** _Script d'import des données openfoodfacts dans MangezMieux_
    * **static/** _CSS + JS_
    * **templates/** _HTML_
    * **urls.py** _Fichiers de redirection des urls_
* **README.md** _Ce fichier_
* **scripts/**


## Packaging

Le projet contient également les sources du paquet Debian.


### Compilation

Pour compiler les paquet, vous aurez besoin des outils de packaging Debian [voir ici](http://www.debian.org/doc/manuals/maint-guide/start.en.html).

Vous pourrez ensuite le compiler en executant la commande :

    dpkg-buildpackage

On passera ensuite une étape de vérification du paquet avec lintian : 

    lintian -b ../mangezmieux_X.X-X_all.deb

### Installation

Il ne vous reste plus qu'à installer le paquet sur le serveur en exécutant la commande : 

    dpkg -i mangezmieux_X.X-X_all.deb || apt-get install -f

**/!\ Sur une Debian squeeze il faut installer django via les backports pour avoir la version 1.4 :**

Ajouter le dépot au fichier `/etc/apt/sources.list`

    deb http://backports.debian.org/debian-backports squeeze-backports main contrib non-free

Installer django 1.4

    apt-get -t squeeze-backports install python-django


