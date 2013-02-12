from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^liste/?$', 'produit.views.liste'),
    url(r'^show/(?P<id>\d*)/$', 'produit.views.show'),
)