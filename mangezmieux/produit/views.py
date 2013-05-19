#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from core.models import *
from planning.forms import *
from forms import *
from django.db.models import Q
from auth.models import *

def liste(request):
    produits = Produit.objects.all().order_by('nom')
    return render(request, 'produit/liste.html', locals())

def detail(request, id):
	
    """
       Ajout d'un produit dans un repas dans la base
    """
    try:
	produit = Produit.objects.get(pk=id)
    except Recette.DoesNotExist:
	raise Http404
    
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
            
            return redirect('/planning/?d=' + str(d))
    else:
	form = RepasProduitForm()
        
        convs = Conversion.objects.filter(uniteBase = produit.unite)      
	form.fields["unite"].choices = [(conv.uniteSpecifique.pk, conv.uniteSpecifique.nom) for conv in convs]
	form.fields["produit"].initial = produit.nom
	ordre = request.session.get('ordre')
	date = request.session.get('date')
	
	form.fields["ordre"].initial = ordre
	form.fields["date"].initial = date
        
        profil = ProfilUtilisateur.objects.get(user = request.user)
        
        form.fields["nbPersonne"].initial = profil.nbPersonnes
	try:
		del request.session['ordre']
		del request.session['date']
	except KeyError:
		pass
    
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
						
				produits = produits.order_by('nom')
				return render(request, 'produit/recherche.html', locals())

	else:
		form = FormulaireRechercheProduits()
	return render(request, 'produit/recherche.html', locals())

def type(request, id=-1):
	if id == -1:
		types = TypeProduit.objects.filter(parent__isnull=True).order_by('nom')
		return render(request, 'produit/types.html', locals())
	else:
		try:
			type = TypeProduit.objects.get(pk=id)
			produits = Produit.objects.filter(Q(type_produit=type.id)).order_by('nom')
			return render(request, 'produit/type_liste.html', locals())
		except TypeProduit.DoesNotExist:
			raise Http404

