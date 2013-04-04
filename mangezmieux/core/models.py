#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from mysqlfulltextsearch.search_manager import SearchManager

#Tag des recettes,goûts
class Tag(models.Model):
    texte = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.texte
    
#Unité de mesure pour les quantités
class Unite(models.Model):
    nom = models.CharField(max_length=25, unique=True)
    abreviation = models.CharField(max_length=4)

    def __unicode__(self):
        return self.nom

#Type de produit (proteines, féculents...)
class TypeProduit(models.Model):
    nom = models.CharField(max_length=15, unique=True)
    parent = models.ForeignKey('self', null = True, blank = True)

    def __unicode__(self):
        return self.nom

#Valeurs nutritionnelles pour 100g
class ValeurNutritionnelle(models.Model):
	energie = models.IntegerField() #en kJ
	proteines = models.IntegerField(null=True)
	glucides = models.IntegerField(null=True)
	lipides = models.IntegerField(null=True)
	fibres = models.IntegerField(null=True)
	sodium = models.IntegerField(null=True)

	def __unicode__(self):
		return unicode(self.energie)

#Produit
class Produit(models.Model):
    nom = models.CharField(max_length=25, unique=True)
    type_produit = models.ForeignKey(TypeProduit, related_name='types')
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)
    valeur_nutritionnelle = models.ForeignKey(ValeurNutritionnelle)
    image = models.ImageField(upload_to='produit/', null = True, blank = True)

    def __unicode__(self):
        return self.nom

#Ligne de recette : quantité d'un produit
class LigneRecette(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)

    def __unicode__(self):
        return u'%d %s %s' % (self.quantite, self.unite, self.produit)      

#Ligne de produit : quantité d'un produit (utile pour des repas personnalisés)
class LigneProduit(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)

    def __unicode__(self):
        return u'%d %s %s' % (self.quantite, self.unite, self.produit)      
	
#Categorie : Categorie de la recette (Dessert, Entree...)
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nom
        
#Recette : composition (lignes) et instructions
class Recette(models.Model):
    nom = models.CharField(max_length=100)    
    lignes = models.ManyToManyField(LigneRecette)
    instructions = models.TextField()
    duree = models.IntegerField()
    difficulte = models.IntegerField()
    createur = models.ForeignKey(User)
    est_valide = models.BooleanField()
    categorie = models.ManyToManyField(Categorie)
    image = models.ImageField(upload_to='recette/', null = True, blank = True)
    #tags = models.ManyToManyField(Tag, null = True, blank = True)
    tags = models.CharField(max_length=500, null = True, blank = True)
    objects = SearchManager()
    
    def __unicode__(self):
        return self.nom


#Repas : Repas à un moment donné à une date
# Note  : Vérifier à l'insertion qu'il y a bien SOIT une recette SOIT un produit
class Repas(models.Model):
    date = models.DateField()
    ordre = models.IntegerField()
    nb_personne = models.IntegerField()
    recette = models.ManyToManyField(Recette, null = True, blank = True)
    produit = models.ManyToManyField(LigneProduit, null = True, blank = True)
    utilisateur = models.ForeignKey(User)

#Commande : commande à une date
class Commande(models.Model):
    date = models.DateTimeField()
    client = models.ForeignKey(User, null = False, blank = False)
    
    def __unicode__(self):
        return self.date    
    
#LigneCommande : une ligne issue d'une commande
class LigneCommande(models.Model):
    produit = models.ForeignKey(Produit, null = False, blank = False)
    commande = models.ForeignKey(Commande, null = False, blank = False, related_name='lignes')
    
    def __unicode__(self):
        return self.produit
    
#Repas non persiste
class RepasNonPersiste():
    date = models.DateField()
    ordre = models.IntegerField()
    
class LignePanier(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    
class Panier(models.Model):
    utilisateur = models.ForeignKey(User)
    lignes = models.ManyToManyField(LignePanier, null = True, blank = True)
    
#Recette favorite
class RecetteFavorite(models.Model):
    recette = models.ForeignKey(Recette, null = False, blank = False)
    utilisateur = models.ForeignKey(User, null = False, blank = False)

    def __unicode__(self):
        return u'%s %s' % (self.recette.nom, unicode(self.utilisateur))
