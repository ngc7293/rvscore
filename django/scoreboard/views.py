

from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from .models import Time, Car
from .utils import *

# Create your views here.
def index(request):
    return render(request, 'scoreboard/index.html')


def track_normal(request, track):
    return redirect('track_category', track=track, mode='normal', category='global')


def track_global(request, track, mode):
    return redirect('track_category', track=track, mode=mode, category='global')


def track_category(request, track, mode, category):
    track = track.replace('-',' ')
    times = Time.objects.filter(track=track, mode=mode).order_by('time')

    if category != 'global':
        times = times.filter(car__category=category)
    
    times = times[:10]
    context = {
        'times': times,
        'track': track.capitalize(),
        'mode' : mode.capitalize() if mode != 'reversemirror' else 'Reverse Mirror',
        'category': category.capitalize() 
    }
    return render(request, 'scoreboard/score.html', context)


@csrf_exempt
def sync(request):
    if request.method == 'POST':
        new = add_times_from_json(request.body)
        return HttpResponse(str(new))
    if request.method == 'GET':
        payload = get_times_json()
        return HttpResponse(payload)