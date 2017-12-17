

from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from .models import Time, Car
from .utils import *

# Create your views here.
def scoreboard(request):
    return render(request, 'scoreboard/index.html')

def scoreboard_json(request, track, mode, category):
    track = track.replace('-',' ')
    times = Time.objects.filter(track=track, mode=mode).order_by('time')

    if category != 'global':
        times = times.filter(car__category=category)

    return render(request, 'scoreboard/score.json', {'times': times[:10]})

@csrf_exempt
def sync(request, count=1):
    if request.method == 'POST':
        new = add_times_from_json(request.body)
        return HttpResponse(str(new))

    if request.method == 'GET':
        payload = get_times_json(count)
        return HttpResponse(payload)