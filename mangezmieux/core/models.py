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
<<<<<<< HEAD

=======
    parent = models.ForeignKey('self', null = True)
    
>>>>>>> ajout du modele et du planning
    def __unicode__(self):
        return self.nom

#Produit
class Produit(models.Model):
    nom = models.CharField(max_length=25)
<<<<<<< HEAD
    type_produit = models.ForeignKey(TypeProduit)
    image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
=======
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)
    valeur_energetique = models.IntegerField()
    type_produit = models.ForeignKey(TypeProduit)
    #image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
>>>>>>> ajout du modele et du planning
    
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
<<<<<<< HEAD
    image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
=======
    duree = models.IntegerField()
    difficulte = models.IntegerField()
    est_valide = models.BooleanField()
    #image = models.ImageField(upload_to='/var/www/mangezmieux/mangezmieux/upload/')
>>>>>>> ajout du modele et du planning
    
    def __unicode__(self):
        return self.nom

#Categorie : Categorie de la recette (Dessert, Entree...)
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nom

#Ligne de recette : quantité d'un produit
class LigneProduit(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    unite = models.ForeignKey(Unite)

    def __unicode__(self):
        return u'%d %s %s' % (self.quantite, self.unite, self.produit)

#Repas : Repas à un moment donnée à une date
class Repas(models.Model):
    date = models.DateField()
    ordre = models.IntegerField()
    nb_personne = models.IntegerField()
    recette = models.ForeignKey(Recette, null = True, blank = True)
    produit = models.ManyToManyField(LigneProduit, null = True, blank = True)

