from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    #Application URLs
    url(r'^inscription/$', 'auth.views.inscription'),
    url(r'^connexion/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    url(r'^deconnexion/$', 'django.contrib.auth.views.logout', {'template_name': 'auth/loggedout.html'}),
    url(r'^mon_compte/$', 'auth.views.compte'),
    url(r'^changer_mot_de_passe/$', 'django.contrib.auth.views.password_change', {'template_name': 'auth/changer_mdp.html'}),
    url(r'^mot_de_passe_change/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'auth/changer_mdp_done.html'}),
    url(r'^mot_de_passe_oublie/$', 'django.contrib.auth.views.password_reset', {'template_name': 'auth/reset_mdp.html', 'email_template_name':'auth/reset_mdp_email.html'}),
    url(r'^confirmation_mot_de_passe_oublie/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'auth/reset_mdp_confirm.html', 'post_reset_redirect' : '/mote_de_passe_redefini'}),
    url(r'^mot_de_passe_envoye/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'auth/reset_mdp_done.html'}),
    url(r'^mot_de_passe_redefini/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'auth/reset_mdp_complete.html'}),
)
