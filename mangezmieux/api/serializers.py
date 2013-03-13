#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from core.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')
                
class UniteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unite
		fields = ('nom', 'abreviation')
		
class TypeProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = TypeProduit
		fields = ('id', 'nom',)
		
class ProduitSerializer(serializers.ModelSerializer):
	type_produit = TypeProduitSerializer()
	stypeProduit = TypeProduitSerializer()
	unite = UniteSerializer()
	class Meta:
		model = Produit
		fields = ('id','nom', 'quantite', 'valeur_energetique', 'type_produit', 'stype_produit', 'unite','image')
		
class LigneRecetteSerializer(serializers.ModelSerializer):
	produit = ProduitSerializer()
	unite = UniteSerializer()
	class Meta:
		model = LigneRecette
		fields = ('produit', 'quantite', 'unite')
		
class LigneProduitSerializer(serializers.ModelSerializer):
	produit = ProduitSerializer()
	unite = UniteSerializer()
	class Meta:
		model = LigneProduit
		fields = ('produit', 'quantite', 'unite')
		
class CategorieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categorie
		fields = ('nom',)
		
class CommandeSerializer(serializers.ModelSerializer):
	client = UserSerializer()
	class Meta:
		model = Commande
		fields = ('date', 'client')
		
class LigneCommandeSerializer(serializers.ModelSerializer):
	commande = CommandeSerializer()
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

class RepasSerializer(serializers.ModelSerializer):
	utilisateur = UserSerializer()
	produit = ProduitSerializer()
	recette = RecetteSerializer()
	class Meta:
		model = Repas
		fields = ('date', 'ordre', 'nb_personne','utilisateur', 'produit', 'recette')

