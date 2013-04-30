#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404 
from core.models import *
from django.contrib.auth.decorators import login_required
from auth.models import *
from django.forms.formsets import formset_factory, BaseFormSet
from datetime import *

@login_required(login_url='/connexion')
def home(request):
    """
        Page d'accueil des commandes de l'utilisateur
    """
    # récupération des commandes de l'utilisateur connecté, triées par ordre décroissant
    commandes = Commande.objects.filter(client = request.user).order_by('-date')
    
    return render(request, 'commande/home.html', locals())

@login_required(login_url='/connexion')
def detail(request, id):
    """
        fonction d'affichage du détail d'une commande
    """
    commande = Commande.objects.get(pk = id)

    return render(request, 'commande/detail.html', locals())

@login_required(login_url='/connexion')
def commander(request):
    """
        fonction permettant de commander le panier dont l'identifiant est passé en paramètre
    """
    idPanier = request.POST.get('idPanier', None)

    # si panier il y a
    if idPanier != None:
        panier = Panier.objects.get(pk = idPanier)

        creationCommande(panier, request.user)
        
        return redirect('/commande/')
    else:
        return redirect('/panier/')

def creationCommande(_panier, _user):
    """
        Fonction métier permetant de créer une commande à partir d'un panier et d'un utilisateur
    """
    # création de la nouvelle commande
    commande = Commande()
    commande.date = date.today()
    commande.client = _user
    commande.numero = creationNumeroCommande()

    commande.save()

    # on remplit les lignes de commandes à partir des lignes de panier
    for lignePanier in _panier.lignes.all():
        ligne = LigneCommande()
        ligne.commande = commande
        ligne.produit = lignePanier.produit
        ligne.quantite = lignePanier.quantite
        ligne.save()

    # desctruction du panier concerné
    _panier.delete()

def creationNumeroCommande():
    """
        Fonction permettant de générer un numéro de commande
    """
    commandes = Commande.objects.filter(date = date.today())

    numeroCommande = "CMD" + date.today().strftime("%d%m%Y") + "-" + str(commandes.count())

    return numeroCommande
