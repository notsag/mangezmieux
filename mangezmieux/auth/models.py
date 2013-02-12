#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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
		if created:
			ProfilUtilisateur.objects.create(user=instance)

	post_save.connect(create_profil_utilisateur, sender=User)
	
