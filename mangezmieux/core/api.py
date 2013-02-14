#-*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request, format=None):
	"""
	API
	"""
	return Response({
		'users': reverse('user-list', request=request),
	})

