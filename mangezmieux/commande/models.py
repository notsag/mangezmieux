#-*- coding: utf-8 -*-
from django.db import models
from produit.models import *
from django.contrib.auth.models import User

#Commande : commande à une date
class Commande(models.Model):
    date = models.DateTimeField()
    client = models.ForeignKey(User, null = False, blank = False)
    numero = models.CharField(max_length=20, null = True, blank = True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.numero, unicode(self.client))
    
#LigneCommande : une ligne issue d'une commande
class LigneCommande(models.Model):
    produit = models.ForeignKey(Produit, null = False, blank = False)
    quantite = models.IntegerField()
    commande = models.ForeignKey(Commande, null = False, blank = False, related_name='lignes')
    
    def __unicode__(self):
        return u'%s - %s' % (self.commande.numero, unicode(self.produit))

