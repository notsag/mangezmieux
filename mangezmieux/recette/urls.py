from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^show/(?P<id>\d*)/$', 'recette.views.show'),
	url(r'^recherche$', 'recette.views.recherche'),
)
