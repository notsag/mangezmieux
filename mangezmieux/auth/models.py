#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

class ProfilUtilisateur(models.Model):
	"""
	Classe permettant d'ajouter un profil à la classe User de Django.
	Pour utiliser cette classe, il faut s'assurer que la 
	variable AUTH_PROFILE_MODULE du fichier settings.py
	pointe bien vers cette classe : 
	AUTH_PROFILE_MODULE = 'auth.ProfilUtilisateur'
	"""
	user = models.OneToOneField(User)

	def __unicode__(self):
			return unicode(self.user)

	def create_profil_utilisateur(sender, instance, created, **kwargs):
		"""
		Création automatique du profil à la création d'un User
		"""
		if created:
			ProfilUtilisateur.objects.create(user=instance)

	
	def create_auth_token(sender, instance, created, **kwargs):
		"""
		Création automatique du token utilisateur (pour l'API)
		"""
		if created:
			Token.objects.create(user=instance)


	post_save.connect(create_profil_utilisateur, sender=User)
	post_save.connect(create_auth_token, sender=User)

	
