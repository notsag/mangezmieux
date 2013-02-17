from django.shortcuts import render
from core.models import *
from planning.forms import *

def liste(request):
	recettes = Recette.objects.filter(est_valide=True)
	return render(request, 'recette/liste.html', locals())

def show(request, id):
	recettes = Recette.objects.filter(pk=id, est_valide=True)
	form = RepasForm()
	if recettes.count() > 0 :
		recette = recettes[0]
		form.fields["recette"].initial = recette.nom
	return render(request, 'recette/show.html',locals())
