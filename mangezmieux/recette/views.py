#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from core.models import *
from forms import SearchForm
from planning.forms import *

def detail(request, id):
	try:
		recette = Recette.objects.get(pk=id, est_valide=True)
		form = RepasRecetteForm()

		# recette = recettes[0]
		form.fields["recette"].initial = recette.nom
		ordre = request.session.get('ordre')
		date = request.session.get('date')
		
		form.fields["ordre"].initial = ordre
		form.fields["date"].initial = date
		try:
			del request.session['ordre']
			del request.session['date']
		except KeyError:
			pass
	except Recette.DoesNotExist:
		raise Http404

	return render(request, 'recette/detail.html',locals())

def recherche(request):
	"""fonction de recherche multicritères de recettes"""
	#une fois le formulaire soumis
	if len(request.GET) > 0:
		form = SearchForm(request.GET)
		if form.is_valid():
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

			return render(request, 'recette/recherche.html', locals())
	else:
		form = SearchForm()

	return render(request, 'recette/recherche.html', locals())
	
def categorie(request, id=-1):
	if id == -1 :
		categories = Categorie.objects.all()
		return render(request, 'recette/categories.html',locals())
	else :
		try:
			categorie = Categorie.objects.get(pk=id)
			recettes = Recette.objects.filter(categorie=id, est_valide=True)
			return render(request, 'recette/categorie_liste.html', locals())
		except Categorie.DoesNotExist:
			raise Http404
