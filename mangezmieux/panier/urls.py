#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', 'panier.views.home'),
    url(r'^ajouter/(?P<id>\d*)/$', 'panier.views.ajouter'),
    url(r'^supprimer/(?P<id>\d*)/$', 'panier.views.supprimer'),
    url(r'^generer/$', 'panier.views.generer'),
)
