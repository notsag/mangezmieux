#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import inscription

urlpatterns = patterns('',
	url(r'^', inscription),
)
