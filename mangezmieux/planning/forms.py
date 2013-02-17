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

class RepasForm(forms.Form):
    """
	Formulaire d'ajout de repas avec : 
		recette,
		ordre, 
		nbPersonne, 
		date, 
    """
    recette = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    ordre = forms.ChoiceField(choices=ORDRE_CHOICES, required=True)
    nbPersonne = forms.IntegerField(min_value = 1)
    date = forms.DateField(required=True)