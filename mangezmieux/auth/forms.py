#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms


class FormulaireInscription(forms.Form):
	"""
	Formulaire d'inscription avec : 
		username,
		nom, 
		prénom, 
		email unique, 
		mot de passe avec confirmation

	"""
	username = forms.RegexField(regex=r'^[\w.@+-]+$',max_length=30,widget=forms.TextInput(),label=_("Identifiant"),error_messages={'Invalide': _("L'identifiant ne peut contenir que des caractères alphanumériques, \"@\",\".\",\"+\",\"-\" et\" _\".")})
    nom = forms.CharField(widget=forms.TextInput(), label="Nom")
    prenom = forms.CharField(widget=forms.TextInput(), label="Prénom")
    email = forms.EmailField(widget=forms.TextInput(),label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),label="Confirmation du mot de passe")
    

    def clean(self):
		"""
			Fonction vérifiant que les deux mots de passe sont bien identiques
		"""
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Les deux mots de passe sont différents."))
        return self.cleaned_data

    def clean_email(self):
		"""
			Fonction vérifiant que l'adresse email n'est pas déjà utilisée
		"""
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("Cette adresse email est déjà associée à un compte."))
        return self.cleaned_data['email']

