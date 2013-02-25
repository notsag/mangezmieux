from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^liste/?$', 'produit.views.liste'),
    url(r'^detail/(?P<id>\d*)/$', 'produit.views.detail'),
	url(r'recherche/$', 'produit.views.recherche'),
)
