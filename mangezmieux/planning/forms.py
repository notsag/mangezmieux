#-*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from core.models import *

ORDRE_CHOICES = (
        (0, 'Petit déjeuner'),
        (1, 'Déjeuner'),
        (2, 'Dîner'),
    )

class RepasRecetteForm(forms.Form):
    """
	Formulaire d'ajout de recette à un repas avec : 
		recette,
		ordre, 
		nbPersonne, 
		date, 
    """
    recette = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    ordre = forms.ChoiceField(choices=ORDRE_CHOICES, required=True)
    nbPersonne = forms.IntegerField(min_value = 1, required=True)
    date = forms.DateField(required=True)


class RepasProduitForm(forms.Form):
    """
	Formulaire d'ajout de produit à un repas avec : 
		produit,
                quantite,
                unite,
		ordre, 
		nbPersonne, 
		date, 
    """
    produit = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    quantite = forms.IntegerField(min_value = 1, required=True)
    unite = forms.ChoiceField(choices=[(unite.pk, unite.nom) for unite in Unite.objects.all()]	, required=True)
    ordre = forms.ChoiceField(choices=ORDRE_CHOICES, required=True)
    nbPersonne = forms.IntegerField(min_value = 1, required=True)
    date = forms.DateField(required=True)
