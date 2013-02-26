from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('home.urls')),
    url(r'^produit/', include('produit.urls')),
    url(r'^planning/', include('planning.urls')),
    url(r'^recette/', include('recette.urls')),
    url(r'', include('auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
	url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {
		'document_root' : settings.MEDIA_ROOT
	}),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
