#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from core.models import *
from forms import SearchForm
from planning.forms import *
from django.contrib.auth.decorators import login_required
from auth.models import *

def detail(request, id):
	"""
		Ajout d'une recette dans un repas dans la base
	"""
	try:
		recette = Recette.objects.get(pk=id, est_valide=True)
	except Recette.DoesNotExist:
		raise Http404
	
	if request.method == 'POST':
	    form = RepasRecetteForm(data=request.POST, files=request.FILES) #On reprend les données
	    if form.is_valid():
		r = form.cleaned_data['recette']
		o = form.cleaned_data['ordre']
		d = form.cleaned_data['date']
		n = form.cleaned_data['nbPersonne']
		
		recette = Recette.objects.filter(nom = r)[0]
		
		#On vérifie si on a un repas à ce moment
		repas = Repas.objects.filter(date = d, utilisateur = request.user, ordre = o)
		if repas.count() == 0:
		    repas = Repas()
		else:
		    repas = repas[0]
		
		repas.date = d
		repas.nb_personne = n
		repas.ordre = o
		repas.utilisateur = request.user
		repas.save()
		repas.recette.add(recette)
		repas.save()
		
		return redirect('/planning')
	else:
		form = RepasRecetteForm()
		
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
	
	try:
		recette = Recette.objects.get(pk=id, est_valide=True)
		
		user = request.user
		recetteFavorite = RecetteFavorite.objects.filter(utilisateur = user, recette = recette)
		estFavorite = False
		if recetteFavorite.count() != 0:
			estFavorite = True

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

def ajout_favoris(request, id):
    """
        Fonction permettant d'ajouter une recette comme favorite pour un utilisateur connecté
    """
    user = request.user
    recette = Recette.objects.filter(pk = id)[0]

    favoris = RecetteFavorite.objects.filter(utilisateur = user, recette = recette)

    if favoris.count() == 0:
         recetteFavorite = RecetteFavorite()
         
         recetteFavorite.recette = recette
         recetteFavorite.utilisateur = user
         recetteFavorite.save()

    return redirect('/recette/detail/'+ str(recette.pk) + '/')

def retrait_favoris(request, id):
    """
        Fonction permettat de retirer une recette favorivte pour l'utilisateur connecté
    """
    user = request.user
    recette = Recette.objects.filter(pk = id)[0]

    favoris = RecetteFavorite.objects.filter(utilisateur = user, recette = recette)

    if favoris.count() != 0:
        recetteFavorite = favoris[0]
        recetteFavorite.delete()

    return redirect('/recette/detail/' + str(recette.pk) + '/')

@login_required(login_url='/connexion')
def suggestion(request):
	'''
		Suggestion de recettes par rapport aux gouts
	'''
	#Recuperation du user, de ses gouts, de ses repas
	u = request.user
	profil = ProfilUtilisateur.objects.get(user = u)
	
	gouts = profil.gouts
	repass = Repas.objects.filter(utilisateur = profil)
	
	#On fait un tableau d'occurence contenant l'occurence des recettes utilisées
	pref ={}
	for repas in repass :
		for recette in repas.recette.all():
			if recette.id in pref:
				pref[recette.id] = pref[recette.id] + 1
			else:
				pref[recette.id] = 0
	
	#On parcourt notre liste de gout et on récupere les recettes ayant ce goût
	for gout in gouts.all():
		recettes = Recette.objects.filter(tags__in=[gout])
		for recette in recettes:
			if recette.id in pref:
				pref[recette.id] = pref[recette.id] + 1
			else:
				pref[recette.id] = 0
	
	#On fait une liste avec les recettes à proposer
	recettesProp = []
	
	for key in pref.keys():
		if pref[key] == 0:
			recette = Recette.objects.get(id = key)
			recettesProp.append(recette)
	
	return render(request, 'recette/suggestion.html', locals())
