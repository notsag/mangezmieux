Projet Mangez Mieux

Site Web en Python/Django répondant au besoin : mangez varié et équilibré sans vous fatiguer!

=======================================================================================
Architecture : Django-app
=======================================================================================
mangezmieux/
  |- core/           #fichiers du coeur de l'application
  |  |- admin.py     #déclaration des objets administrables
  |  |- models.py    #"classes" de l'application
  |  |- tests.py     #tests unitaires
  |  |- views.py     #fichier de traitement des infos à passer au template
  |- home/           #pages liées à un simple utilisateur
  |  |- urls.py      #fichiers de redirection des urls
  |  |- models.py    #"classes" de l'application
  |  |- tests.py     #tests unitaires
  |  |- views.py     #fichier de traitement des infos à passer au template
  |  |- __init__.py  #fichier package
  |- static/         #fichiers statiques (css/js)
  |  |- bootstrap/   #fichiers de bootstrap
  |  |- style.css    #fichier css
  |- templates/      #fichiers templates
  |  |- home/        #templates liés à home
  |  |- base.html    #structure de base de l'application
  |- __init__.py     #fichier package
  |- manage.py       #script admin django
  |- settings.py     #parametres de l application
  |- urls.py         #fichiers de redirection des urls
TEMPLATES/


