#-*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request, format=None):
	"""
	API
	"""
	return Response({
		'users': reverse('user-list', request=request),
                'repas': reverse('repas-list', request=request),
                'produits': reverse('produit-list', request=request),
                'recette': reverse('recette-list', request=request),
                'unite': reverse('unite-list', request=request),
                'typeProduits': reverse('typeproduit-list', request=request),
                'ligneRecettes': reverse('lignerecette-list', request=request),
                'ligneProduits': reverse('ligneproduit-list', request=request),
                'categories': reverse('categorie-list', request=request),
                'commandes': reverse('commande-list', request=request),
                'ligneCommandes': reverse('lignecommande-list', request=request),
		'lignePaniers': reverse('lignepanier-list', request=request),
		'paniers': reverse('panier-detail', request=request),
	})

