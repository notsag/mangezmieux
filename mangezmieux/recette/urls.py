from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^show/(?P<id>\d*)/$', 'recette.views.show'),
	url(r'^search/$', 'recette.views.search'),
	url(r'^liste/$', 'recette.views.liste'),
)
