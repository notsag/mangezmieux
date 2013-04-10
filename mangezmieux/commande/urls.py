#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^commander/?$', 'commande.views.commander'),
    url(r'^detail/(?P<id>\d*)/$', 'commande.views.detail'),
    url(r'^/?$', 'commande.views.home'),
)
