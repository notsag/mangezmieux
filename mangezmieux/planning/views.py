# Create your views here
from collections import defaultdict
from datetime import *
from django.shortcuts import render
from core.models import *
import time
from dateutil import parser

def home(request):
    
    #On recupere la date passee en parametre get
    dateS = request.GET.get('d', None)
    if dateS != None:
        try:
            dateC = parser.parse(dateS).date()
        except:
            dateC = date.today()
    else:
        dateC = date.today()
    
    #On calcule la date de debut de semaine
    debutSemaine = dateC
    debutSemaineJour = debutSemaine.strftime('%A')
    while debutSemaineJour != "Monday":
        debutSemaine = debutSemaine + timedelta(days=-1)
        debutSemaineJour = debutSemaine.strftime('%A')
    
    #On calcule la date de fin de semaine    
    finSemaine = dateC
    finSemaineJour = debutSemaine.strftime('%A')
    while finSemaineJour != "Sunday":
        finSemaine = finSemaine + timedelta(days=1)
        finSemaineJour = finSemaine.strftime('%A')
        
    if date.today() < finSemaine and date.today() > debutSemaine:
        ok = True
        day = date.today().strftime('%A')
        
    repass = Repas.objects.filter(date__gte = debutSemaine, date__lte = finSemaine).order_by('date','ordre')
    
    
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
    
    #On recupere une date de la semaine precedente et une date de la semaine suivante
    semainePrecedente = dateC + timedelta(days=-7)
    semaineSuivante = dateC + timedelta(days=7)
    
    #planning = defaultdict(defaultdict)
    
    #for repas in repass :
    #    planning[repas.date.strftime('%A')][repas.ordre] = repas
    
    return render(request, 'planning/home.html', locals())