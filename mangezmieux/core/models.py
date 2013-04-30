#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from produit.models import *
from recette.models import *
from commande.models import *
from home.models import *
from panier.models import *

#Repas non persiste
class RepasNonPersiste():
    date = models.DateField()
    ordre = models.IntegerField()
    recette = models.BooleanField()
    produit = models.BooleanField()
    
class Conversion(models.Model):
    uniteSpecifique = models.ForeignKey(Unite,related_name='specifique')
    uniteBase = models.ForeignKey(Unite,related_name='base')
    multiplicateur = models.FloatField()
