#-*- coding: utf-8 -*-
from serializers import *
from core.api import *

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
        if dateDebut != None and dateFin != None:
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
