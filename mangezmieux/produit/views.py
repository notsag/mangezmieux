# Create your views here.
from django.shortcuts import render
from core.models import *

def liste(request):
    produits = Produit.objects.all()
    return render(request, 'produit/liste.html', locals())

def show(request, name_produit):
    produit = Produit.objects.filter(nom=name_produit)
    return render(request, 'produit/show.html', locals())