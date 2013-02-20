from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', 'planning.views.home'),
    url(r'^ajouter/?$', 'planning.views.ajouter_repas'),
)
