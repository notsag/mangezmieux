#-*- coding: utf-8 -*-
from serializers import *
from core.api import *
import time
from dateutil import parser
from datetime import *
from auth.models import *
from core.api import *
from planning.views import *

class RecetteSuggestion(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of recettes.
    """
    model = Recette
    serializer_class = RecetteSerializer
    
    def get_queryset(self):
	userId = self.request.QUERY_PARAMS.get('u', None)
	user = User.objects.get(id = userId)
        return suggestion(user)
	    
class UserList(generics.ListCreateAPIView):
	"""
	Point de l'API pour lister les utilisateurs
	"""
	model = User
	serializer_class = UserSerializer
					
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Point de l'API pour afficher les infos d'un utilisateur
	"""
	model = User
	serializer_class = UserSerializer
        
class RepasList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of repas.
    """
    model = Repas
    serializer_class = RepasSerializer
    
    def get_queryset(self):
        dateDebut = self.request.QUERY_PARAMS.get('dd', None)
        dateFin = self.request.QUERY_PARAMS.get('df', None)
	userId = self.request.QUERY_PARAMS.get('u', None)
        if dateDebut != None and dateFin != None and userId != None:
	    user = User.objects.filter(id = userId)
	    if user != None:
		return Repas.objects.filter(date__gte = dateDebut, date__lte = dateFin, utilisateur = user).order_by('date','ordre')
	    else:
		return Repas.objects.filter(date__gte = dateDebut, date__lte = dateFin).order_by('date','ordre')
        else:
            return Repas.objects.all()
    
class RepasDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents repas
    """
    model = Repas
    serializer_class = RepasSerializer

class ProduitList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of products.
    """
    model = Produit
    serializer_class = ProduitSerializer

    def get_queryset(self):
        # récupération des paramètres
        nom = self.request.QUERY_PARAMS.get('nom', None)
        typeP = self.request.QUERY_PARAMS.get('typeP', None)
        valeur = self.request.QUERY_PARAMS.get('valeur', None)
        
        # application des critères
        produits = Produit.objects.all()

        # si le nom est renseigné
        if nom != '' and nom != None:
            produits = produits.filter(nom__icontains=nom)

        # si le type est renseigné
        if typeP != '' and typeP != None:
            produits = produits.filter(type_produit=typeP)

        # si la valeur énergétique est renseignée
        if valeur != '' and typeP != None:
            if valeur <= '500':
                produits = produits.filter(valeur_energetique__lte=valeur)
            else:
                produits = produits.filter(valeur_energetique__gte=valeur)

        return produits

class ProduitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents product
    """
    model = Produit
    serializer_class = ProduitSerializer
    
class RecetteList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of recettes.
    """
    model = Recette
    serializer_class = RecetteSerializer

    def get_queryset(self):
        #récupération des paramètres
        nom = self.request.QUERY_PARAMS.get('nom', None)
        duree = self.request.QUERY_PARAMS.get('duree', None)
        difficulteRecup = self.request.QUERY_PARAMS.get('difficulte', None)
        categorieRecup = self.request.QUERY_PARAMS.get('categorie', None)

        # application des critères
        recettes = Recette.objects.filter(est_valide=True)

        # si le nom est renseigné
        if nom != '' and nom != None:
            recettes = recettes.filter(nom__icontains=nom)

        # si la durée est renseignée
        if duree != '' and duree != None and duree > '0':
            if duree <= '90':
                recettes = recettes.filter(duree__lte=duree)
            else:
                recettes = recettes.filter(duree__gte=duree)

        # si la difficulté est renseignée
        if difficulteRecup != '' and difficulteRecup != None:
            recettes = recettes.filter(difficulte=difficulteRecup)

        if categorieRecup != '' and categorieRecup != None:
            recettes = recettes.filter(categorie=categorieRecup)

        return recettes

class RecetteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents recette
    """
    model = Recette
    serializer_class = RecetteSerializer
    
class UniteList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of unites.
    """
    model = Unite
    serializer_class = UniteSerializer
        
class UniteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents unite
    """
    model = Unite
    serializer_class = UniteSerializer
    
class TypeProduitList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of type produits.
    """
    model = TypeProduit
    serializer_class = TypeProduitSerializer
        
class TypeProduitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents type produit
    """
    model = TypeProduit
    serializer_class = TypeProduitSerializer
    
class LigneRecetteList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of type ligneRecette.
    """
    model = LigneRecette
    serializer_class = LigneRecetteSerializer
        
class LigneRecetteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents type LigneRecette
    """
    model = LigneRecette
    serializer_class = LigneRecetteSerializer
    
class LigneProduitList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of type LigneProduit.
    """
    model = LigneProduit
    serializer_class = LigneProduitSerializer
        
class LigneProduitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents type LigneProduit
    """
    model = LigneProduit
    serializer_class = LigneProduitSerializer
    
class CategorieList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of type Categorie.
    """
    model = Categorie
    serializer_class = CategorieSerializer
        
class CategorieDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents type Categorie
    """
    model = Categorie
    serializer_class = CategorieSerializer
    
class CommandeList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of type Commande.
    """
    model = Commande
    serializer_class = CommandeSerializer
        
class CommandeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents type Commande
    """
    model = Commande
    serializer_class = CommandeSerializer
    
class LigneCommandeList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of type LigneCommande.
    """
    model = LigneCommande
    serializer_class = LigneCommandeSerializer
        
class LigneCommandeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents type LigneCommande
    """
    model = LigneCommande
    serializer_class = LigneCommandeSerializer
