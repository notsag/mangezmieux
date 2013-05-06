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
    planning = remplirPlanning(repass, debutSemaine)
    
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
    
    return render(request, 'planning/home4.html', locals())

def remplirPlanning(repass, debutSemaine):
    planning = []
    for i in xrange(3):
        planning.append([])
        for j in xrange(7):
            repasVide = RepasNonPersiste()
            repasVide.date = debutSemaine + timedelta(days= j)
            repasVide.ordre = i
            repasVide.nb_personne = 0
            repasVide.recette = False
	    repasVide.produit = False
            planning[i].append(repasVide)
    
    for repas in repass :
        if repas.date.strftime('%A') == 'Monday':
            planning[repas.ordre][0] = repas
        elif repas.date.strftime('%A') == 'Tuesday':
            planning[repas.ordre][1] = repas
        elif repas.date.strftime('%A') == 'Wednesday':
            planning[repas.ordre][2] = repas
        elif repas.date.strftime('%A') == 'Thursday':
            planning[repas.ordre][3] = repas
        elif repas.date.strftime('%A') == 'Friday':
            planning[repas.ordre][4] = repas
        elif repas.date.strftime('%A') == 'Saturday':
            planning[repas.ordre][5] = repas
        elif repas.date.strftime('%A') == 'Sunday':
            planning[repas.ordre][6] = repas
    
    return planning

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
    r = request.GET.get('r', None)

    _user = request.user

    repas = Repas.objects.filter(date = d, utilisateur = _user, ordre = o)[0]
    retirerRecetteRepasMetier(repas, r)

    return redirect('/planning')

def retirer_produit_repas(request):
    """Fonction permettant de retirer un produit d'un repas du planning"""
    d = request.GET.get('d', None)
    o = request.GET.get('o', None)
    p = request.GET.get('p', None)

    _user = request.user

    repas = Repas.objects.filter(date = d, utilisateur = _user, ordre = o)[0]
    retirerProduitRepasMetier(repas, p)

    return redirect('/planning')

def retirerRecetteRepasMetier(_repas, _recetteId):
    """
        Fonction métier permettant de retirer une recette d'un repas
    """
    recette = Recette.objects.get(pk = _recetteId)

    try:
        _repas.recette.remove(recette)
        _repas.save()

        if _repas.recette.all().count() == 0 and _repas.produit.all().count() == 0:
            _repas.delete()
    except:
        print("Erreur : recette non présente pour le repas")

def retirerProduitRepasMetier(_repas, _produitId):
    """
        Fonction métier permettant de retirer une ligne produit d'un repas
    """
    produit = LigneProduit.objects.get(pk = _produitId)

    try:
        _repas.produit.remove(produit)
        produit.delete()
        _repas.save()

        if _repas.recette.all().count() == 0 and _repas.produit.all().count() == 0:
            _repas.delete()
    except:
        print("Erreur : produit non présente pour le repas")

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

@login_required(login_url='/connexion')
def genererPlanning(request):
    
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
    planning = remplirPlanning(repass, debutSemaine)
    
    for jour in planning:
	for ordre in jour:
            if ordre.nb_personne == 0:
                #Si petit dej
                if ordre.ordre == 0:
                    recette = Recette.objects.filter(categorie__in=Categorie.objects.filter(nom='Dessert')).order_by('?')[:1].get()
                    repas = Repas()
                    repas.date = ordre.date
                    repas.nb_personne = 1
                    repas.ordre = ordre.ordre
                    repas.utilisateur = user
                    repas.save()
                    repas.recette.add(recette)
                    repas.save()
                #Si dej ou diner
                if ordre.ordre == 1 or ordre.ordre == 2:
                    recette = Recette.objects.filter(categorie__in=Categorie.objects.filter(nom='Entrée')).order_by('?')[:1].get()
                    repas = Repas()
                    repas.date = ordre.date
                    repas.nb_personne = 1
                    repas.ordre = ordre.ordre
                    repas.utilisateur = user
                    repas.save()
                    repas.recette.add(recette)
                    repas.save()
                    
                    recette = Recette.objects.filter(categorie__in=Categorie.objects.filter(nom='Plat')).order_by('?')[:1].get()
                    repas.recette.add(recette)
                    repas.save()
                    
                    recette = Recette.objects.filter(categorie__in=Categorie.objects.filter(nom='Dessert')).order_by('?')[:1].get()
                    repas.recette.add(recette)
                    repas.save()

    return redirect('/planning?d='+str(dateC))