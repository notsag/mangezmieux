#-*- coding: utf-8 -*-
from django.db import models

class Produit(models.Model):
    nom = models.CharField(primary_key=True, max_length=25)
    TYPE_CHOICES = (('V','Viande'),('P','Poisson'),('F','Féculent'),('L','Légume'),('PL','Produit laitier'), ('A','Autre'))
    type_produit = models.CharField(max_length=25, choices=TYPE_CHOICES)
    #image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
    
    def __unicode__(self):
        return self.nom

class LigneRecette(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    UNIT_CHOICES = (('g', 'Grammes'), ('mL', 'Millilitres'), ('càc', 'Cuillère à café'), ('càs', 'Cuillère à soupe'), ('p','Pièce'))
    unite = models.CharField(max_length=25, choices=UNIT_CHOICES, null=True)

    def __unicode__(self):
        return u'%d %s %s' % (self.quantite, self.unite, self.produit)

class Recette(models.Model):
    nom = models.CharField(primary_key=True,max_length=100)
    lignes = models.ManyToManyField(LigneRecette)
    #instructions = models.CharField(max_length=500)
    #image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
    
    def __unicode__(self):
        return self.nom

