#-*- coding: utf-8 -*-
from django.shortcuts import redirect, render_to_response, render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from forms import *
from recette.models import *
from datetime import *
from core.models import *

@login_required(login_url='/connexion')
def stats(request):
	user = request.user
    
	"""
	    On recupere la date passee en parametre get
	"""
	dateS = request.GET.get('d', None)
	if dateS != None:
	    try:
		dateC = parser.parse(dateS).date()
	    except:
		dateC = date.today()
	else:
	    dateC = date.today()
	
	"""
	    On calcule la date de debut de semaine
	"""
	debutSemaine = dateC
	debutSemaineJour = debutSemaine.strftime('%A')
	while debutSemaineJour != "Monday":
	    debutSemaine = debutSemaine + timedelta(days=-1)
	    debutSemaineJour = debutSemaine.strftime('%A')
	
	"""
	    On calcule la date de fin de semaine
	"""
	finSemaine = dateC
	finSemaineJour = debutSemaine.strftime('%A')
	while finSemaineJour != "Sunday":
	    finSemaine = finSemaine + timedelta(days=1)
	    finSemaineJour = finSemaine.strftime('%A')
	
	"""
	    On verifie si on est dans la semaine courange pour mettre en valeur le jour courant
	"""
	if date.today() < finSemaine and date.today() > debutSemaine:
	    ok = True
	    day = date.today().strftime('%A')
	
	"""
	    On recupere les repas de la semaine courante
	"""
	if user.is_authenticated():
	    repass = Repas.objects.filter(date__gte = debutSemaine, date__lte = finSemaine, utilisateur = user).order_by('date','ordre')
	else :
	    repass = Repas.objects.filter(date__gte = debutSemaine, date__lte = finSemaine).order_by('date','ordre')
	
	planning = remplirPlanning(repass, debutSemaine)
	
	stats = []
	for i in xrange(7):
	    stats.append([])
	    for j in xrange(5):
		stats[i].append(0)
	
	i = 0
	for jour in planning:
		proteine = 0
		glucide = 0
		lipide = 0
		fibre = 0
		sodium = 0
		for ordre in jour:
			if ordre.recette != False :
				for recette in ordre.recette.all():
					for ligne in recette.lignes.all():
						proteine = proteine + ligne.produit.valeur_nutritionnelle.proteines
						glucide = glucide + ligne.produit.valeur_nutritionnelle.glucides
						lipide = lipide + ligne.produit.valeur_nutritionnelle.lipides
						fibre = fibre + ligne.produit.valeur_nutritionnelle.fibres
						sodium = sodium + ligne.produit.valeur_nutritionnelle.sodium
			if ordre.recette != False :
				for ligne in ordre.produit.all():
					proteine = proteine + ligne.produit.valeur_nutritionnelle.proteines
					glucide = glucide + ligne.produit.valeur_nutritionnelle.glucides
					lipide = lipide + ligne.produit.valeur_nutritionnelle.lipides
					fibre = fibre + ligne.produit.valeur_nutritionnelle.fibres
					sodium = sodium + ligne.produit.valeur_nutritionnelle.sodium
		
		stats[i][0] = proteine
		stats[i][1] = glucide
		stats[i][2] = lipide
		stats[i][3] = fibre
		stats[i][4] = sodium
		i = i + 1
	
	return render(request, 'auth/stats.html', locals())	

def remplirPlanning(repass, debutSemaine):
	planning = []
	for i in xrange(7):
	    planning.append([])
	    for j in xrange(3):
		repasVide = RepasNonPersiste()
		repasVide.date = debutSemaine + timedelta(days= i)
		repasVide.ordre = j
		repasVide.nb_personne = 0
		repasVide.recette = False
		repasVide.produit = False
		planning[i].append(repasVide)
	
	for repas in repass :
	    if repas.date.strftime('%A') == 'Monday':
		planning[0][repas.ordre] = repas
	    elif repas.date.strftime('%A') == 'Tuesday':
		planning[1][repas.ordre] = repas
	    elif repas.date.strftime('%A') == 'Wednesday':
		planning[2][repas.ordre] = repas
	    elif repas.date.strftime('%A') == 'Thursday':
		planning[3][repas.ordre] = repas
	    elif repas.date.strftime('%A') == 'Friday':
		planning[4][repas.ordre] = repas
	    elif repas.date.strftime('%A') == 'Saturday':
		planning[5][repas.ordre] = repas
	    elif repas.date.strftime('%A') == 'Sunday':
		planning[6][repas.ordre] = repas
	
	return planning

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

