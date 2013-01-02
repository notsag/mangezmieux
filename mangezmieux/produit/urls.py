from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^liste/?$', 'produit.views.liste'),
)