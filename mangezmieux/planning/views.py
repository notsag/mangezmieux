#-*- coding: utf-8 -*-
from collections import defaultdict
from datetime import *
from django.shortcuts import render, redirect
from core.models import *
import time
from dateutil import parser
from planning.forms import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/connexion')
def home(request):
    
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
    
    """
        On cree un tableau 3*7 qui represente la semaine courante
    """
    planning = []
    for i in xrange(3):
        planning.append([])
        for j in xrange(7):
             planning[i].append(0)
    
    for repas in repass :
        if repas.date.strftime('%A') == 'Monday':
            planning[repas.ordre][0] = repas
        elif repas.date.strftime('%A') == 'Tuesday':
            planning[repas.ordre][1] = repas
        elif repas.date.strftime('%A') == 'Wednesday':
            planning[repas.ordre][2] = repas
        elif repas.date.strftime('%A') == 'Thursday':
            planning[repas.ordre][3] = repas
        elif repas.date.strftime('%A') == 'Friday':
            planning[repas.ordre][4] = repas
        elif repas.date.strftime('%A') == 'Saturday':
            planning[repas.ordre][5] = repas
        elif repas.date.strftime('%A') == 'Sunday':
            planning[repas.ordre][6] = repas
    
    """
        On recupere une date de la semaine precedente et une date de la semaine suivante
    """
    semainePrecedente = dateC + timedelta(days=-7)
    semaineSuivante = dateC + timedelta(days=7)
    
    #planning = defaultdict(defaultdict)
    
    #for repas in repass :
    #    planning[repas.date.strftime('%A')][repas.ordre] = repas
        
    return render(request, 'planning/home.html', locals())

def add_repas(request):
    """
        Ajout d'un repas dans la base
    """
    if request.method == 'POST':
        form = RepasForm(data=request.POST, files=request.FILES) #On reprend les données
        if form.is_valid():
            r = form.cleaned_data['recette']
            o = form.cleaned_data['ordre']
            d = form.cleaned_data['date']
            n = form.cleaned_data['nbPersonne']
            
            recette = Recette.objects.filter(nom = r)[0]
            
            repas = Repas()
            repas.date = d
            repas.nb_personne = n
            repas.recette = recette
            repas.ordre = o
            repas.utilisateur = request.user
            repas.save()
            
            return redirect('/planning')
        
        else:
            return redirect('/')
    