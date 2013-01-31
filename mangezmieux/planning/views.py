# Create your views here.
from django.shortcuts import render
from core.models import *

def home(request):
    repas = Repas.objects.all()
    return render(request, 'planning/home.html', locals())