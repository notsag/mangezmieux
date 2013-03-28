#-*- coding: utf-8 -*-
import pprint
from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth.decorators import login_required
from auth.models import *
from panier.forms import *

def home(request):
    
    paniers = Panier.objects.filter(utilisateur = request.user)
    
    if paniers.count() == 0:
        panier = Panier()
        panier.utilisateur = request.user
        panier.save()
    else:
        panier = paniers[0]
        
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