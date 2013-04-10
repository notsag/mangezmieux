#-*- coding: utf-8 -*-
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from forms import *


def inscription(request):
	"""
	Cette fonction permet :
		- l'affichage du formulaire d'inscription
		- sa vérification et l'insciption de l'utilisateur à partir
		  du formulaire s'il est valide
	"""
	if request.method == 'POST':
		form = FormulaireInscription(data=request.POST, files=request.FILES)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			nom = form.cleaned_data['nom']
			prenom = form.cleaned_data['prenom']
			user = User(username=username, 
			            email=email, 
						last_name=nom,
						first_name=prenom)
			user.set_password(password)
			user.save()
			new_user = authenticate(username=username, password=password)
			login(request, new_user)
			return HttpResponseRedirect('/') #On redirige vers la selection des goûts
	else:
		form = FormulaireInscription()
	return render_to_response('auth/inscription.html',{'form': form,},context_instance=RequestContext(request))

@login_required(login_url='/connexion')
def compte(request):
	"""
	Cette fonction permet d'afficher le formulaire d'édition du compte utilisateur
	"""
	if request.method == 'POST':
		form = FormulaireUtilisateur(request.POST, instance=request.user)
		formp = FormulaireProfil(request.POST, instance=ProfilUtilisateur.objects.get(user=request.user))
		if form.is_valid() and formp.is_valid():
			form.save()
			formp.save()
	else:
		form = FormulaireUtilisateur(instance=request.user)
		formp = FormulaireProfil(instance=ProfilUtilisateur.objects.get(user=request.user))
	return render_to_response('auth/mon_compte.html',locals(),context_instance=RequestContext(request))

