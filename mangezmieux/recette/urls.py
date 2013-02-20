from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^recherche$', 'recette.views.recherche'),
	url(r'^detail/(?P<id>\d*)/$', 'recette.views.detail'),
)
