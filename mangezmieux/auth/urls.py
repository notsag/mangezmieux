from django.conf.urls.defaults import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import UserList, UserDetail

urlpatterns = patterns('',
    #Application URLs
	url(r'^inscription/$', 'auth.views.inscription'),
    url(r'^connexion/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    url(r'^deconnexion/$', 'django.contrib.auth.views.logout', {'template_name': 'auth/loggedout.html'}),
    url(r'^mon_compte/$', 'auth.views.compte'),
	#API URLs
     url(r'^api/utilisateurs/$', UserList.as_view(), name='user-list'),
	 url(r'^api/utilisateurs/(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
	)

