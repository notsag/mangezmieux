#-*- coding: utf-8 -*-
from django import forms
from core.models import *

class FormulaireRechercheProduits(forms.Form):
	"""
	Formulaire de recherche de produits
	"""
	nom = forms.CharField(label='Nom du produit', required=False)
	typeP = forms.ChoiceField(label='Type', choices=(), required=False)
	valeur = forms.ChoiceField(label='Valeur ébergétique', choices=(), required=False)

	def __init__(self, *args, **kwargs):
		super(FormulaireRechercheProduits, self).__init__(*args, **kwargs)
		self.fields['typeP'].choices = [('-1','-')] + [(typeP.pk, typeP.nom) for typeP in TypeProduit.objects.all()]
		self.fields['valeur'].choices = (('-1','-'), ('50','< 50 kcal'), ('100','< 100 kcal'), ('250','< 250 kcal'), ('500','< 500 kcal'), ('501','> 500 kcal'))

