#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from core.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')
                
class RepasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repas
        fields = ('date', 'ordre', 'nb_personne','utilisateur', 'produit', 'recette')
        
class ProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Produit
		fields = ('nom', 'quantite', 'valeur_energetique', 'type_produit', 'stype_produit', 'unite')
		
class UniteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unite
		fields = ('nom', 'abreviation')
		
class TypeProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = TypeProduit
		fields = ('nom', 'parent')
		
class LigneRecetteSerializer(serializers.ModelSerializer):
	class Meta:
		model = LigneRecette
		fields = ('produit', 'quantite', 'unite')
		
class LigneProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = LigneProduit
		fields = ('produit', 'quantite', 'unite')
		
class CategorieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categorie
		fields = ('nom',)
		
class CommandeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Commande
		fields = ('date', 'client')
		
class LigneCommandeSerializer(serializers.ModelSerializer):
	class Meta:
		model = LigneCommande
		fields = ('produit', 'commande')

class RecetteSerializer(serializers.ModelSerializer):
	lignes = LigneRecetteSerializer()
	createur = UserSerializer()
	categorie = CategorieSerializer()
	class Meta:
		model = Recette
		fields = ('nom', 'lignes', 'instructions', 'duree', 'difficulte', 'createur', 'est_valide', 'categorie')

