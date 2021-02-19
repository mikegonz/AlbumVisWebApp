from .albumvis import Visualizer
from .models import Album, Render
from django.shortcuts import render


def index(request):
    track = Visualizer('').currently_playing_track()
    track_name = 'no track currently playing' if track is None else track['item']['name']
    context = {'track': track_name, 'js': {'path': 'uhoh.jpg'}}
    return render(request, 'index.html', context)
