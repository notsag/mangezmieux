from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'type/$', 'produit.views.type'),
	url(r'type/(?P<id>\d*)/$', 'produit.views.type'),
	url(r'recherche/$', 'produit.views.recherche'),
	url(r'^detail/(?P<id>\d*)/$', 'produit.views.detail'),
)
