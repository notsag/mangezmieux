# Create your views here
from collections import defaultdict
from datetime import *
from django.shortcuts import render
from core.models import *

def home(request):

    #On calcule la date de debut de semaine
    debutSemaine = date.today()
    debutSemaineJour = debutSemaine.strftime('%A')
    while debutSemaineJour != "Monday":
        debutSemaine = debutSemaine + timedelta(days=-1)
        debutSemaineJour = debutSemaine.strftime('%A')
    
    #On calcule la date de fin de semaine    
    finSemaine = date.today()
    finSemaineJour = debutSemaine.strftime('%A')
    while finSemaineJour != "Sunday":
        finSemaine = finSemaine + timedelta(days=1)
        finSemaineJour = finSemaine.strftime('%A')
        
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
    
    #planning = defaultdict(defaultdict)
    
    #for repas in repass :
    #    planning[repas.date.strftime('%A')][repas.ordre] = repas
    
    return render(request, 'planning/home.html', locals())