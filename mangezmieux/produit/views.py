# Create your views here.
from django.shortcuts import render

def liste(request):
    produits = Produit.objects.all()
    return render(request, 'produit/liste.html', locals())