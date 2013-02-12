#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

Class Utilisateur(models.Model):
	"""
	Classe utilisateur dérivée de la classe User de Django.
	Pour utiliser cette classe, il faut s'assurer que la 
	variable AUTH_PROFILE_MODULE du fichier settings.py
	pointe bien vers cette classe : 
	AUTH_PROFILE_MODULE = 'auth.Utilisateur'
	"""
	user = models.OneToOneField(User)
	def __unicode__(self):
			return self.user

