#-*- coding: utf-8 -*-
from django import forms
from core.models import *

class SearchForm(forms.Form):
	"""Formulaire de recherche de recettes"""

	#champs du formulaire
	nom = forms.CharField(label='Nom de la recette', required=False)
	duree = forms.ChoiceField(label='Durée', choices=(), required=False)
	difficulte = forms.ChoiceField(label='Difficulté', choices=(), required=False)
	categorie = forms.ChoiceField(label='Catégorie', choices=(), required=False)

	def __init__(self, *args, **kwargs):
		"""Constructeur du formulaire, c'est là que l'on rempli les listes déroulantes"""
		#constucteur de l'objet parent
		super(SearchForm, self).__init__(*args, **kwargs)

		#remplissage des listes
		self.fields['duree'].choices = (('-1', '-'), ('30', '< 30 min'), ('60', '< 1 h'), ('90', '< 1 h 30'), ('91', '> 1 h 30'))
		self.fields['difficulte'].choices = (('-1', '-'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'))
		self.fields['categorie'].choices = [('-1', '-')] + [(cat.pk, cat.nom) for cat in Categorie.objects.all()]		


class AddForm(forms.Form):
	"""Formulaire d'ajout de recettes"""

	#champs du formulaire
	nom = forms.CharField(label='Nom de la recette', required=True)
	instructions = forms.CharField(label='Instructions', required=True, widget=forms.Textarea)
	duree = forms.IntegerField(label='Durée', required=True)
	difficulte = forms.ChoiceField(label='Difficulté', choices=(), required=True)
	categorie = forms.ChoiceField(label='Catégorie', choices=(), required=True)
	tags = forms.CharField(label='Tags (séparés par un espace)', required=True)
	nb_personne = forms.IntegerField(label='Nombre de personnes', required=True)
	#produit = forms.CharField(label='Produit', required=False)
	
	def __init__(self, *args, **kwargs):
		"""Constructeur du formulaire, c'est là que l'on rempli les listes déroulantes"""
		#constucteur de l'objet parent
		super(AddForm, self).__init__(*args, **kwargs)

		#remplissage des listes
		self.fields['difficulte'].choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'))
		self.fields['categorie'].choices = [(cat.pk, cat.nom) for cat in Categorie.objects.all()]		

class LigneRecetteForm(forms.Form):
	#champs du formulaire
	produit = forms.CharField(label='Produit', required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
	quantite = forms.IntegerField(label='Quantité', required=True)
	unite = forms.ChoiceField(label='Unité', choices=(), required=True)
	
	def __init__(self, *args, **kwargs):
		"""Constructeur du formulaire, c'est là que l'on rempli les listes déroulantes"""
		#constucteur de l'objet parent
		super(LigneRecetteForm, self).__init__(*args, **kwargs)

		#remplissage des listes
		self.fields['unite'].choices = [(un.pk, un.nom) for un in Unite.objects.all()]
		
class LigneRecetteForm2(forms.ModelForm):
	class Meta:
		model = LigneRecette