#-*- coding: utf-8 -*-
import pprint
from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth.decorators import login_required
from auth.models import *
from panier.forms import *
from django.forms.formsets import formset_factory, BaseFormSet
from dateutil import parser

def home(request):
    
    paniers = Panier.objects.filter(utilisateur = request.user)
    
    if paniers.count() == 0:
        panier = Panier()
        panier.utilisateur = request.user
        panier.save()
    else:
        panier = paniers[0]
    
    PanierProduitFormset = formset_factory(LignePanierForm, extra=0)
    if request.method == "POST":
        formset = PanierProduitFormset(request.POST)
        if formset.is_valid():
            for form in formset.forms:
                p = form.cleaned_data['produit']
                q = form.cleaned_data['quantite']
                i = form.cleaned_data['id']
                produit = Produit.objects.filter(nom = p)[0]

                ligne = LignePanier.objects.get(pk = i)
                ligne.quantite = q
                ligne.save()

            return render(request, 'panier/home.html', locals())
    else:
        initial =[]
        for ligne in panier.lignes.all():
                initial.append({'id':ligne.id,'produit':ligne.produit.nom, 'quantite':ligne.quantite})

        formset = PanierProduitFormset(initial=initial)
    
        
    return render(request, 'panier/home.html', locals())
    
def ajouter(request, id):
    
    produit = Produit.objects.get(pk = id)
    
    if request.method == 'POST':
        form = PanierProduitForm(data=request.POST, files=request.FILES) #On reprend les donn?es
        if form.is_valid():
            p = form.cleaned_data['produit']
            q = form.cleaned_data['quantite']

            produit = Produit.objects.filter(nom = p)[0]
            
            paniers = Panier.objects.filter(utilisateur = request.user)
            if paniers.count() == 0:
                panier = Panier()
                panier.utilisateur = request.user
                panier.save()
            else:
                panier = paniers[0]
            
            #si on a des lignes dans notre panier on regarde si on n'a pas déjà le produit en question pour juste ajouter la quantite
            if panier.lignes.count() > 0:
                lignes = panier.lignes.filter(produit = produit)
                if lignes.count() == 0:
                    ligne = LignePanier()
                    ligne.produit = produit
                    ligne.quantite = q
                else:
                    ligne = lignes[0]
                    ligne.quantite = q + ligne.quantite
            else :
                ligne = LignePanier()
                ligne.produit = produit
                ligne.quantite = q

            ligne.save()
            
            panier.lignes.add(ligne)
            panier.save()
            
            #request.session['panier'] = panier
            
            return redirect('/panier')
    else:
        form = PanierProduitForm()
        form.fields["produit"].initial = produit.nom
        
    return render(request, 'panier/ajouter.html', locals())


def supprimer(request, id):
    
    ligne = LignePanier.objects.get(pk = id)
    panier = Panier.objects.filter(utilisateur = request.user)[0]
    panier.lignes.remove(ligne)
    panier.save()
    ligne.delete()
    
    return redirect('/panier')
    
def generer(request):
    #On recupere les dates de debut et de fin
    dateDebutString = request.GET.get('dd', None)
    dateFinString = request.GET.get('df', None)
    
    dateDebut = parser.parse(dateDebutString).date()
    dateFin = parser.parse(dateFinString).date()
    
    #On recupere les repas entre cet intervalle
    repass = Repas.objects.filter(date__gte = dateDebut, date__lte = dateFin, utilisateur = request.user).order_by('date','ordre')
    
    prod = {}
    
    for repas in repass:
        for recette in repas.recette.all():
            for ligne in recette.lignes.all():
                #Pour chaque ligne de la recette on recupere la quantite necessaire de produit
                uniteProduit = ligne.produit.unite
                uniteRecette = ligne.unite    
                conv = Conversion.objects.filter(uniteSpecifique = uniteRecette, uniteBase = uniteProduit)[0]
                quantiteRecette = ligne.quantite * conv.multiplicateur
                quantiteRecette = (quantiteRecette * repas.nb_personne) / recette.nb_personne
                
                if ligne.produit in prod:
                    prod[ligne.produit] = prod[ligne.produit] + quantiteRecette
                else:
                    prod[ligne.produit] = quantiteRecette
        for produit in repas.produit.all():
            #Pour chaque ligne de la recette on recupere la quantite necessaire de produit
            uniteProduit = produit.produit.unite
            uniteRecette = produit.unite    
            conv = Conversion.objects.filter(uniteSpecifique = uniteRecette, uniteBase = uniteProduit)[0]
            quantiteRecette = produit.quantite * conv.multiplicateur
            #quantiteRecette = quantiteRecette * repas.nb_personne
            
            if produit.produit in prod:
                prod[produit.produit] = prod[produit.produit] + quantiteRecette
            else:
                prod[produit.produit] = quantiteRecette
    
    panierR = {}
    paniers = Panier.objects.filter(utilisateur = request.user)
    if paniers.count() == 0:
        panier = Panier()
        panier.utilisateur = request.user
        panier.save()
    else:
        panier = paniers[0]
    
    
    #On remplit le nombre de produits necessaire
    for key in prod.keys():
        produit = key
        quantiteNec = prod[key]
        
        #On regarde si on n'a pas déjà des produits utiles dans notre panier
        lignesP = panier.lignes.filter(produit = produit)
        if lignesP.count() > 0:
            quantite = lignesP[0].quantite * lignesP[0].produit.quantite
        else:
            quantite = 0
            
        nbProduit = 0
        while quantite < quantiteNec :
            quantite = quantite + produit.quantite
            nbProduit = nbProduit + 1
        
        panierR[produit] = nbProduit
    
    for key in panierR.keys():
        #si on a des lignes dans notre panier on regarde si on n'a pas déjà le produit en question pour juste ajouter la quantite
        if panier.lignes.count() > 0:
            lignes = panier.lignes.filter(produit = produit)
            if lignes.count() == 0:
                ligne = LignePanier()
                ligne.produit = key
                ligne.quantite = panierR[key]
            else:
                ligne = lignes[0]
                ligne.quantite = panierR[key] + ligne.quantite
        else :
            ligne = LignePanier()
            ligne.produit = key
            ligne.quantite = panierR[key]
    
        ligne.save()
        
        panier.lignes.add(ligne)
        panier.save()
        
    
    return redirect('/panier')
    