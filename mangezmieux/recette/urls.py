from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^detail/(?P<id>\d*)/$', 'recette.views.detail'),
	url(r'^recherche/$', 'recette.views.rechercher'),
)
