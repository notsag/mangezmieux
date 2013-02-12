#-*- coding: utf-8 -*-
from models import ProfilUtilisateur
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

"""
Ajout du profil utilisateur à l'interface d'administration
"""

class ProfilInline(admin.StackedInline):
	model = ProfilUtilisateur
	can_delete = False
	verbose_name_plural = 'profil'

class UserAdmin(UserAdmin):
	inlines = (ProfilInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

