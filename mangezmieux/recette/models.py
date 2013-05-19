#-*- coding: utf-8 -*-
from django.db import models
from produit.models import *
from mysqlfulltextsearch.search_manager import SearchManager
from django.contrib.auth.models import User

#Tag des recettes,goûts
class Tag(models.Model):
    texte = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.texte

#Ligne de recette : quantité d'un produit
class LigneRecette(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)

    class Meta:
        verbose_name_plural = "Lignes de recette"

    def __unicode__(self):
        return u'%d %s %s' % (self.quantite, self.unite, self.produit)      

#Ligne de produit : quantité d'un produit (utile pour des repas personnalisés)
class LigneProduit(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)

    class Meta:
        verbose_name_plural = "Lignes de produit"

    def __unicode__(self):
        return u'%d %s %s' % (self.quantite, self.unite, self.produit)      
	
#Categorie : Categorie de la recette (Dessert, Entree...)
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categorie/', null = True, blank = True)

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
    nb_personne = models.IntegerField()
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

    class Meta:
        verbose_name_plural = "Repas"

#Recette favorite
class RecetteFavorite(models.Model):
    recette = models.ForeignKey(Recette, null = False, blank = False)
    utilisateur = models.ForeignKey(User, null = False, blank = False)

    class Meta:
        verbose_name_plural = "Recettes favorites"

    def __unicode__(self):
        return u'%s %s' % (self.recette.nom, unicode(self.utilisateur))
