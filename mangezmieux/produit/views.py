# Create your views here.
from django.shortcuts import render
from core.models import *
from planning.forms import *

def liste(request):
    produits = Produit.objects.all()
    return render(request, 'produit/liste.html', locals())

def detail(request, id):
    produits = Produit.objects.filter(pk=id)
    form = RepasProduitForm()
    if produits.count() > 0 :
        produit = produits[0]
        form.fields["produit"].initial = produit.nom
        ordre = request.session.get('ordre')
        date = request.session.get('date')
        
        form.fields["ordre"].initial = ordre
        form.fields["date"].initial = date
        try:
                del request.session['ordre']
                del request.session['date']
        except KeyError:
                pass
        
    return render(request, 'produit/detail.html', locals())

