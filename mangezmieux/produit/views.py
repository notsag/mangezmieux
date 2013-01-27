# Create your views here.
from django.shortcuts import render
from core.models import *

def liste(request):
    produits = Produit.objects.all()
    return render(request, 'produit/liste.html', locals())

def show(request, name_produit):
    produits = Produit.objects.filter(nom=name_produit)
    if produits.count() > 0 :
        produit = produits[0]
    return render(request, 'produit/show.html', locals())