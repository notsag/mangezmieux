from django.shortcuts import render
from core.models import *

def liste(request):
	recettes = Recette.objects.filter(est_valide=True)
	return render(request, 'recette/liste.html', locals())

def show(request, id):
	recettes = Recette.objects.filter(pk=id, est_valide=True) 
	if recettes.count() > 0 :
		recette = recettes[0]
	return render(request, 'recette/show.html',locals())
