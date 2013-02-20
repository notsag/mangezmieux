#-*- coding: utf-8 -*-
from django.shortcuts import render
from core.models import *
from forms import SearchForm
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

def search(request):
	"""fonction de recherche multicritères de recettes"""
	#une fois le formulaire soumis
	if len(request.GET) > 0:
		form = SearchForm(request.GET)
		if form.is_valid():
			# à développer
			recettes = Recette.objects.filter(est_valide=True)

			# si un nom est renseigné
			if form.cleaned_data['nom'] != '':
				recettes = recettes.filter(nom__icontains=form.cleaned_data['nom'])

			# si la durée est renseignée
			if form.cleaned_data['duree'] > '0':
				if form.cleaned_data['duree'] <= '90':
					recettes = recettes.filter(duree__lte=form.cleaned_data['duree'])
				else:
					recettes = recettes.filter(duree__gte=form.cleaned_data['duree'])

			# si la difficulté est renseignée
			if form.cleaned_data['difficulte'] != '-1':
				recettes = recettes.filter(difficulte=form.cleaned_data['difficulte'])

			# si la catégorie est renseignée
			if form.cleaned_data['categorie'] != '-1':
				recettes = recettes.filter(categorie=form.cleaned_data['categorie'])

			return render(request, 'recette/search.html', locals())
	else:
		form = SearchForm()

	return render(request, 'recette/search.html', locals())
