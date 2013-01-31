#-*- coding: utf-8 -*-
from django.db import models

#Unité de mesure pour les quantités
class Unite(models.Model):
    nom = models.CharField(max_length=25)
    abreviation = models.CharField(max_length=4)

    def __unicode__(self):
        return self.nom

#Type de produit (proteines, féculents...)
class TypeProduit(models.Model):
    nom = models.CharField(max_length=15)

    def __unicode__(self):
        return self.nom

#Produit
class Produit(models.Model):
    nom = models.CharField(max_length=25)
    type_produit = models.ForeignKey(TypeProduit)
    image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
    
    def __unicode__(self):
        return self.nom

#Ligne de recette : quantité d'un produit
class LigneRecette(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)

    def __unicode__(self):
        return u'%d %s %s' % (self.quantite, self.unite, self.produit)

#Recette : composition (lignes) et instructions
class Recette(models.Model):
    nom = models.CharField(max_length=100)
    lignes = models.ManyToManyField(LigneRecette)
    instructions = models.CharField(max_length=500)
    image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
    
    def __unicode__(self):
        return self.nom

