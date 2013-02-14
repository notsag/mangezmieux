from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    #Application URLs
    url(r'^inscription/$', 'auth.views.inscription'),
    url(r'^connexion/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    url(r'^deconnexion/$', 'django.contrib.auth.views.logout', {'template_name': 'auth/loggedout.html'}),
    url(r'^mon_compte/$', 'auth.views.compte'),
)