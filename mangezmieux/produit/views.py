# Create your views here.
from django.shortcuts import render
from core.models import *

def liste(request):
    produits = Produit.objects.all()
    return render(request, 'produit/liste.html', locals())

def show(request, id):
    produits = Produit.objects.filter(pk=id)
    if produits.count() > 0 :
        produit = produits[0]
    return render(request, 'produit/show.html', locals())

