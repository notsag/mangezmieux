#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from produit.models import *

class LignePanier(models.Model):
    produit = models.ForeignKey(Produit)
    quantite = models.IntegerField()
    
class Panier(models.Model):
    utilisateur = models.ForeignKey(User)
    lignes = models.ManyToManyField(LignePanier, null = True, blank = True)
