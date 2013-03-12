from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', 'planning.views.home'),
    url(r'^ajouter-recette/?$', 'planning.views.ajouter_recette_repas'),
    url(r'^ajouter-produit/?$', 'planning.views.ajouter_produit_repas'),
    url(r'^ajouter-repas/?$', 'planning.views.ajouter_repas'),
    url(r'^retirer-recette/?$', 'planning.views.retirer_recette_repas'),
)
