#-*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from core.models import *

class PanierProduitForm(forms.Form):
    """
	Formulaire d'ajout de produit dans le panier: 
		produit,
                quantite,
    """
    produit = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    quantite = forms.IntegerField(min_value = 1, required=True)
    
class LignePanierForm(forms.Form):
    """
	Formulaire de modification de ligne panier: 
		produit,
                quantite,
    """
    produit = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    quantite = forms.IntegerField(min_value = 1, required=True)
    id = forms.IntegerField(widget=forms.HiddenInput())