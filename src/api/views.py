from .albumvis import Visualizer
from django.shortcuts import render


def index(request):
    track_name = 'no username provided'
    context = {'track': track_name, 'js': {'path': 'uhoh.jpg'}}
    return render(request, 'api/index.html', context)


def playing(request, username):
    track = Visualizer(username).currently_playing_track()
    track_name = 'no track currently playing' if track is None else track['item']['name']
    context = {'track': track_name, 'js': {'path': 'uhoh.jpg'}}
    return render(request, 'api/index.html', context)
