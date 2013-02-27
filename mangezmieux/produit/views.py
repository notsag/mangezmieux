#-*- coding: utf-8 -*-
from django.shortcuts import render
from core.models import *
from planning.forms import *
from forms import *

def liste(request):
    produits = Produit.objects.all()
    return render(request, 'produit/liste.html', locals())

def detail(request, id):
	try:
		produit = Produit.objects.get(pk=id)
		form = RepasProduitForm()
		
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
	except Produit.DoesNotExist:
		raise Http404
		
	return render(request, 'produit/detail.html', locals())

def recherche(request):
	"""
	Recherche multicritères de produits
	"""
	if len(request.GET) > 0:
			form = FormulaireRechercheProduits(request.GET)
			if form.is_valid():
				#on liste tout puis on filtre
				produits = Produit.objects.all()
				
				#critère nom
				if form.cleaned_data['nom'] != '':
					produits = produits.filter(nom__icontains=form.cleaned_data['nom'])

				#critère type
				if form.cleaned_data['typeP'] != '-1':
					produits = produits.filter(type_produit=form.cleaned_data['typeP'])

				#critère valeur énergétique
				if form.cleaned_data['valeur'] != '-1':
					if form.cleaned_data['valeur'] <= '500':
						produits = produits.filter(valeur_energetique__lte=form.cleaned_data['valeur'])
					else:
						produits = produits.filter(valeur_energetique__gte=form.cleaned_data['valeur'])
						
				return render(request, 'produit/recherche.html', locals())

	else:
		form = FormulaireRechercheProduits()
	return render(request, 'produit/recherche.html', locals())
