#-*- coding: utf-8 -*-
from models import News
from django.shortcuts import render

def home(request):
	"""
	Affichage de la home page
	"""
	#On récupère les 5 dernières news en date
	latest_news = News.objects.all().order_by('-date_pub')[:5]
	context = {'latest_news':latest_news}
	return render(request, 'home/home.html', context)

