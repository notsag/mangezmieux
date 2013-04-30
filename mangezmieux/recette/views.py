#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404,HttpResponse
from core.models import *
from forms import *
from planning.forms import *
from django.contrib.auth.decorators import login_required
from auth.models import *
from django.forms import *
from django.core.context_processors import csrf
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet
from recette.forms import *

def detail(request, id):
	"""
		Ajout d'une recette dans un repas dans la base
	"""
	try:
		recette = Recette.objects.get(pk=id, est_valide=True)
	except Recette.DoesNotExist:
		raise Http404
	cateId = request.GET.get('id', None)
	cateName = request.GET.get('name', None)
	
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
		
		if request.user.is_authenticated():
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

def ajouter_recette_favorite(_user, _recette):
    """
        Fonction métier permettant d'ajouter une recette (dont l'identifiant est passé comme paramètre) comme favorite pour l'utilisateur passé en paramètre
    """
    favoris = RecetteFavorite.objects.filter(utilisateur = _user, recette = _recette)

    if favoris.count() == 0:
        recetteFavorite = RecetteFavorite()
        recetteFavorite.recette = _recette
        recetteFavorite.utilisateur = _user
        recetteFavorite.save()

def rechercher_recette_favorite(_user):
    """
        Fonction permettant de trouver la liste des recettes favorites d'un utilisateur passé en paramètre
    """
    return RecetteFavorite.objects.filter(utilisateur = _user)

def ajout_favoris(request, id):
    """
        Fonction permettant d'ajouter une recette comme favorite pour un utilisateur connecté
    """
    user = request.user
    recette = Recette.objects.filter(pk = id)[0]

    ajouter_recette_favorite(user, recette)

    return redirect('/recette/detail/'+ str(recette.pk) + '/')

def retirer_recette_favorite(_user, _recette):
    """
        Fonction permettant de retirer une recette (passée en paramètre) des favoris de l'utilisateur passé en paramètre
    """
    favoris = RecetteFavorite.objects.filter(utilisateur = _user, recette = _recette)

    if favoris.count() != 0:
        recetteFavorite = favoris[0]
        recetteFavorite.delete()

def retrait_favoris(request, id):
    """
        Fonction permettant de retirer une recette favorite pour l'utilisateur connecté
    """
    user = request.user
    recette = Recette.objects.filter(pk = id)[0]

    retirer_recette_favorite(user, recette)

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
	chaines = ''
	for gout in gouts.all():
		chaines += gout.texte + " "
		
	recettes = Recette.objects.search(chaines).order_by("-relevance") 
	for recette in recettes:
		if recette.id in pref:
			pref[recette.id] = pref[recette.id] + 1
		else:
			pref[recette.id] = 0
	
	#On recupere ses recettes favorites
        recettesFav = RecetteFavorite.objects.filter(utilisateur = profil)
        for recetteFav in recettesFav:
		if recetteFav.id in pref:
			pref[recetteFav.id] = pref[recetteFav.id] + 1
		else:
			pref[recetteFav.id] = 0

	#On fait une liste avec les recettes à proposer
	recettesProp = []
	
	for key in pref.keys():
		if pref[key] == 0:
			if len(recettesProp) <= 5:
				recette = Recette.objects.get(id = key)
				recettesProp.append(recette)
	
	return render(request, 'recette/suggestion.html', locals())

@login_required(login_url='/connexion')
def ajouter_recette(request):
	'''
		Ajout d'une nouvelle recette
	'''
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = False
	LigneRecetteFormSet = formset_factory(LigneRecetteForm2, formset=RequiredFormSet)
	if request.method == "POST":
		formset = LigneRecetteFormSet(request.POST)
		form = AddForm(data=request.POST, files=request.FILES) #On reprend les données
		if form.is_valid() and formset.is_valid():
			nom = form.cleaned_data['nom']
			instructions = form.cleaned_data['instructions']
			duree = form.cleaned_data['duree']
			difficulte = form.cleaned_data['difficulte']
			categorie = form.cleaned_data['categorie']
			tags = form.cleaned_data['tags']
			nb_personne = form.cleaned_data['nb_personne']
			
			categorie = Categorie.objects.get(id = categorie)
			
			recette = Recette()
			recette.nom = nom
			recette.createur = request.user
			recette.difficulte = difficulte
			recette.duree = duree
			recette.instructions = instructions
			recette.tags = tags
			recette.nb_personne = nb_personne
			recette.save()
			
			if categorie != None:
				recette.categorie.add(categorie)
			
			for forml in formset.forms:
				'''produit = forml.cleaned_data['produit']
				unite = forml.cleaned_data['unite']
				quantite = forml.cleaned_data['quantite']
				
				produit = Produit.objects.get(nom = produit)
				unite = Unite.objects.get(id = unite)
				
				ligne = LigneRecette()
				ligne.produit = produit
				ligne.unite = unite
				ligne.quantite = quantite
				'''
				
				ligne = forml.save(commit = False)
				
				ligne.save()
				recette.lignes.add(ligne)
			
			recette.save()
		else:
			return render(request, 'recette/ajouter.html', locals())
	else:
		form = AddForm()
		formset = LigneRecetteFormSet()
		
	c = {'form' : form,
	     'formset' : formset
	     }
	
	c.update(csrf(request))
	
	return render(request, 'recette/ajouter.html', locals())

@login_required(login_url='/connexion')
def mes_recettes(request):
    """
        fonction permettant d'obtenir la page "mes recettes"
    """
    recettes = recettesParCreateur(request.user)

    return render(request, 'recette/mesrecettes.html', locals())
    
def recettesParCreateur(_user):
    """
        fonction métier permettant d'obtenir la liste des recettes créées par l'utilisateur passé en paramètre
    """
    if _user != None:
        return Recette.objects.filter(createur = _user)

def get_produit(request):
	val = request.GET.get('v', '')
	if val != None and val != '':
		produits = Produit.objects.filter(nom__icontains = val)
		recettes = Recette.objects.filter(nom__icontains = val)
		html = "<ul>"
		for produit in produits:
			#html += "<li onClick=addForm(this,\"form\",\""+produit.nom+"\")>" + produit.nom + "</li>"
			html += "<li><a href=\"/produit/detail/" + str(produit.id) + "\">" + produit.nom + "</a></li>"
		
		for recette in recettes:
			#html += "<li onClick=addForm(this,\"form\",\""+produit.nom+"\")>" + produit.nom + "</li>"
			html += "<li><a href=\"/recette/detail/" + str(recette.id) +"\">" + recette.nom + "</a></li>"
			
		html+="</ul>"
	else:
		html=""
	return HttpResponse(html)
