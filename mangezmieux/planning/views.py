#-*- coding: utf-8 -*-
from collections import defaultdict
from datetime import *
from django.shortcuts import render, redirect
from core.models import *
import time
from dateutil import parser
from planning.forms import *
from django.contrib.auth.decorators import login_required
from auth.models import *

@login_required(login_url='/connexion')
def home(request):
    
    user = request.user
    
    """
        On recupere la date passee en parametre get
    """
    dateS = request.GET.get('d', None)
    if dateS != None:
        try:
            dateC = parser.parse(dateS).date()
        except:
            dateC = date.today()
    else:
        dateC = date.today()
    
    """
        On calcule la date de debut de semaine
    """
    debutSemaine = dateC
    debutSemaineJour = debutSemaine.strftime('%A')
    while debutSemaineJour != "Monday":
        debutSemaine = debutSemaine + timedelta(days=-1)
        debutSemaineJour = debutSemaine.strftime('%A')
    
    """
        On calcule la date de fin de semaine
    """
    finSemaine = dateC
    finSemaineJour = debutSemaine.strftime('%A')
    while finSemaineJour != "Sunday":
        finSemaine = finSemaine + timedelta(days=1)
        finSemaineJour = finSemaine.strftime('%A')
    
    """
        On verifie si on est dans la semaine courange pour mettre en valeur le jour courant
    """
    if date.today() < finSemaine and date.today() > debutSemaine:
        ok = True
        day = date.today().strftime('%A')
    
    """
        On recupere les repas de la semaine courante
    """
    if user.is_authenticated():
        repass = Repas.objects.filter(date__gte = debutSemaine, date__lte = finSemaine, utilisateur = user).order_by('date','ordre')
    else :
        repass = Repas.objects.filter(date__gte = debutSemaine, date__lte = finSemaine).order_by('date','ordre')
    
    """
        On cree un tableau 3*7 qui represente la semaine courante
    """
    planning = []
    for i in xrange(7):
        planning.append([])
        for j in xrange(3):
            repasVide = RepasNonPersiste()
            repasVide.date = debutSemaine + timedelta(days= i)
            repasVide.ordre = j
            repasVide.nb_personne = 0
            planning[i].append(repasVide)
    
    for repas in repass :
        if repas.date.strftime('%A') == 'Monday':
            planning[0][repas.ordre] = repas
        elif repas.date.strftime('%A') == 'Tuesday':
            planning[1][repas.ordre] = repas
        elif repas.date.strftime('%A') == 'Wednesday':
            planning[2][repas.ordre] = repas
        elif repas.date.strftime('%A') == 'Thursday':
            planning[3][repas.ordre] = repas
        elif repas.date.strftime('%A') == 'Friday':
            planning[4][repas.ordre] = repas
        elif repas.date.strftime('%A') == 'Saturday':
            planning[5][repas.ordre] = repas
        elif repas.date.strftime('%A') == 'Sunday':
            planning[6][repas.ordre] = repas
    
    """
        On recupere une date de la semaine precedente et une date de la semaine suivante
    """
    semainePrecedente = dateC + timedelta(days=-7)
    semaineSuivante = dateC + timedelta(days=7)
    
    #planning = defaultdict(defaultdict)
    
    #for repas in repass :
    #    planning[repas.date.strftime('%A')][repas.ordre] = repas
    
    
    #On recupere les suggestion de recettes
    recettesProp = suggestion(request.user)
    
    return render(request, 'planning/home2.html', locals())

@login_required(login_url='/connexion')
def ajouter_repas(request):
    """
        Ajout d'un repas
    """

    o = request.GET.get('o', None)
    d = request.GET.get('d', None)
    t = request.GET.get('t', None)

    request.session['ordre'] = o
    request.session['date'] = d
    if t == "r":
        return redirect('/recette/recherche/')
    else:
        return redirect('/produit/recherche/')
          
def ajouter_recette_repas(request):
    """
        Ajout d'une recette dans un repas dans la base
    """
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
        
    return render(request, 'recette/detail.html', locals())
        
def ajouter_produit_repas(request):
    """
       Ajout d'un produit dans un repas dans la base
    """
    if request.method == 'POST':
        form = RepasProduitForm(data=request.POST, files=request.FILES) #On reprend les données
        if form.is_valid():
            p = form.cleaned_data['produit']
            q = form.cleaned_data['quantite']
            u = form.cleaned_data['unite']
            o = form.cleaned_data['ordre']
            d = form.cleaned_data['date']
            n = form.cleaned_data['nbPersonne']
            
            produit = Produit.objects.filter(nom = p)[0]
            unite = Unite.objects.filter(pk = u)[0]
            
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
            
            ligneProduit = LigneProduit()
            ligneProduit.produit = produit
            ligneProduit.quantite = q
            ligneProduit.unite = unite
            ligneProduit.save()
            
            repas.produit.add(ligneProduit)
            repas.save()
            
            return redirect('/planning')
            
    return render(request, 'produit/detail.html', locals())

def retirer_recette_repas(request):
    """Fonction permettant de retirer une recette d'un repas du planning"""
    d = request.GET.get('d', None)
    o = request.GET.get('o', None)
    t = request.GET.get('t', None)
    r = request.GET.get('r', None)

    repas = Repas.objects.filter(date = d, utilisateur = request.user, ordre = o)[0]
    recette = Recette.objects.filter(pk = r)[0]

    repas.recette.remove(recette)
    repas.save()

    return redirect('/planning')
    
def suggestion(user):
	'''
		Suggestion de recettes par rapport aux gouts
	'''
        
        dateC = date.today()
        debut = dateC + timedelta(days=-15)
        fin = dateC + timedelta(days=15)
        
	#Recuperation du user, de ses gouts, de ses repas
	u = user
	profil = ProfilUtilisateur.objects.get(user = u)
	
	gouts = profil.gouts
	repass = Repas.objects.filter(date__gte = debut, date__lte = fin, utilisateur = profil)
	
	#On fait un tableau d'occurence contenant l'occurence des recettes utilisées
	pref ={}
	for repas in repass :
		for recette in repas.recette.all():
			if recette.id in pref:
				pref[recette.id] = pref[recette.id] + 1
			else:
				pref[recette.id] = 1
	
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
	
	return recettesProp
