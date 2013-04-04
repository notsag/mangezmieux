Projet Mangez Mieux

Site Web en Python/Django répondant au besoin : mangez varié et équilibré sans vous fatiguer!


Dépendances : django (>= 1.4), djangorestframework, markdown, pyyaml django-filter, python-dateutil

=======================================================================================
Architecture : Django-app
=======================================================================================
mangezmieux/
  |- api/            # module API
  |  |- models.py
  |  |- serializers.py #définition de la sérialisation des objets du core
  |  |- tests.py
  |  |- urls.py
  |  |- views.py  
  |- auth/           #module d'authentification
  |  |- forms.py     #formulaire de création de compte
  |  |- models.py    #classe Utilisateur dérivée du module django.contrib.auth
  |  |- tests.py
  |  |- views.py
  |- core/           #fichiers du coeur de l'application
  |  |- admin.py     
  |  |- models.py    
  |  |- tests.py     
  |  |- views.py    
  |- home/           #pages liées à un simple utilisateur
  |  |- urls.py    
  |  |- models.py  
  |  |- tests.py  
  |  |- views.py 
  |- recette/		 #pages liées aux recettes
  |  |- urls.py
  |  |- forms.py	 #formulaire de recherche de recette
  |  |- views.py
  |- static/         #fichiers statiques (css/js)
  |  |- bootstrap/   #fichiers de bootstrap
  |  |- style.css    #fichier css
  |- templates/      #fichiers templates
  |  |- home/        #templates liés à home
  |  |- base.html    #structure de base de l'application
  |- manage.py       #script admin django
  |- settings.py     #parametres de l application
  |- urls.py         #fichiers de redirection des urls
scripts/
  |- data.csv		 #données de openfoodfacts (liste de produits)
  |- openfoodfacts_to_mangezmieux.pl #script d'import des données openfoodfacts dans MangezMieux


