#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from core.models import *
from rest_framework import serializers

class RecetteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Recette
		fields = ('url', 'nom', 'lignes', 'instructions', 'duree', 'difficulte', 'createur', 'est_valide', 'categorie')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'first_name', 'last_name')
                
class RepasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repas
        fields = ('url', 'date', 'ordre', 'nb_personne','utilisateur', 'produit', 'recette')
        
class ProduitSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Produit
		fields = ('url', 'nom', 'quantite', 'valeur_energetique', 'type_produit', 'stype_produit', 'unite')
		
class UniteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Unite
		fields = ('url', 'nom', 'abreviation')
		
class TypeProduitSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = TypeProduit
		fields = ('url', 'nom', 'parent')
		
class LigneRecetteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = LigneRecette
		fields = ('url', 'produit', 'quantite', 'unite')
		
class LigneProduitSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = LigneProduit
		fields = ('url', 'produit', 'quantite', 'unite')
		
class CategorieSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Categorie
		fields = ('url', 'nom')
		
class CommandeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Commande
		fields = ('url', 'date', 'client')
		
class LigneCommandeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = LigneCommande
		fields = ('url', 'produit', 'commande')
