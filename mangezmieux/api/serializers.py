#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from core.models import *
from home.models import News
from rest_framework import serializers


class NewsSerializer(serializers.ModelSerializer):
	class Meta:
		model = News
		fields = ('id', 'nom', 'info', 'date_pub')

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name')
                
class UniteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unite
		fields = ('id', 'nom', 'abreviation')
		
class TypeProduitSerializer(serializers.ModelSerializer):
	class Meta:
		model = TypeProduit
		fields = ('id', 'nom',)

class ValeurNutritionnelleSerializer(serializers.ModelSerializer):
	class Meta:
		model = ValeurNutritionnelle
		fields = ('id', 'energie', 'proteines', 'glucides', 'lipides', 'fibres', 'sodium')	

class ProduitSerializer(serializers.ModelSerializer):
	type_produit = TypeProduitSerializer()
	valeur_nutritionnelle = ValeurNutritionnelleSerializer()
	unite = UniteSerializer()
	class Meta:
		model = Produit
		fields = ('id','nom', 'quantite', 'valeur_nutritionnelle', 'type_produit', 'unite','image')
		
class LigneRecetteSerializer(serializers.ModelSerializer):
	produit = ProduitSerializer()
	unite = UniteSerializer()
	class Meta:
		model = LigneRecette
		fields = ('id', 'produit', 'quantite', 'unite')
		
class LigneProduitSerializer(serializers.ModelSerializer):
	produit = ProduitSerializer()
	unite = UniteSerializer()
	class Meta:
		model = LigneProduit
		fields = ('id', 'produit', 'quantite', 'unite')
		
class CategorieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Categorie
		fields = ('id','nom',)
		
class CommandeSerializer(serializers.ModelSerializer):
	client = UserSerializer()
	class Meta:
		model = Commande
		fields = ('id', 'date', 'client')
		
class LigneCommandeSerializer(serializers.ModelSerializer):
	commande = CommandeSerializer()
	class Meta:
		model = LigneCommande
		fields = ('id', 'produit', 'commande')

class RecetteSerializer(serializers.ModelSerializer):
	lignes = LigneRecetteSerializer()
	createur = UserSerializer()
	categorie = CategorieSerializer()
	class Meta:
		model = Recette
		fields = ('id','nom', 'nb_personne', 'lignes', 'instructions', 'duree', 'difficulte', 'createur', 'est_valide', 'categorie','image')

class RepasSerializer(serializers.ModelSerializer):
	utilisateur = UserSerializer()
	produit = ProduitSerializer()
	recette = RecetteSerializer()
	class Meta:
		model = Repas
		fields = ('id', 'date', 'ordre', 'nb_personne','utilisateur', 'produit', 'recette')

class RecetteFavoriteSerializer(serializers.ModelSerializer):
	utilisateur = UserSerializer()
	recette = RecetteSerializer()

	class Meta:
		model = RecetteFavorite
		fields = ('id', 'utilisateur', 'recette')

class LignePanierSerializer(serializers.ModelSerializer):
	produit = ProduitSerializer()
	class Meta:
		model = LignePanier
		fields = ('id', 'produit', 'quantite')


class PanierSerializer(serializers.ModelSerializer):
	lignes = LignePanierSerializer()
	utilisateur = UserSerializer()
	class Meta:
		model = Panier
		fields = ('id', 'utilisateur', 'lignes')

