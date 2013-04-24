#-*- coding: utf-8 -*-
from django.db import models

#Unité de mesure pour les quantités
class Unite(models.Model):
    nom = models.CharField(max_length=25, unique=True)
    abreviation = models.CharField(max_length=4)

    def __unicode__(self):
        return self.nom

#Type de produit (proteines, féculents...)
class TypeProduit(models.Model):
    nom = models.CharField(max_length=30, unique=True)
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
    nom = models.CharField(max_length=100, unique=True)
    type_produit = models.ForeignKey(TypeProduit, related_name='types')
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)
    valeur_nutritionnelle = models.ForeignKey(ValeurNutritionnelle)
    image = models.ImageField(upload_to='produit/', null = True, blank = True)

    def __unicode__(self):
        return self.nom




