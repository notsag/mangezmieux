from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^liste/?$','recette.views.liste'),
	url(r'^show/(?P<id>\d*)/$', 'recette.views.show'),
)
