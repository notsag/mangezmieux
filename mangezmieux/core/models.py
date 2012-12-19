#-*- coding: utf-8 -*-
from django.db import models

class Product(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    TYPE_CHOICES = ('Viande', 'Poisson', 'Féculent', 'Légume', 'Produit laitier')
    product_type = models.CharField(max_length=25, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.name

class RecipeLine(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    UNIT_CHOICES = (('g', 'Grammes'), ('mL', 'millilitres'), ('càc', 'Cuillère à café'), ('càs', 'Cuillère à soupe'))
    unit = models.CharField(max_length=25, choices=UNIT_CHOICES, null=True)
    
    def __unicode__(self):
        return u'%d %s %s' % (self.quantity, self.unit, self.product)

class Recipe(models.Model):
    name = models.CharField(primary_key=True,max_length=100)
    lines = models.ManyToManyField(RecipeLine)

    def __unicode__(self):
        return self.name

