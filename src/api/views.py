from .albumvis import Visualizer
from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    track_name = 'no username provided'
    context = {'track': track_name, 'js': {'path': 'uhoh.jpg'}}
    return render(request, 'api/index.html', context)


def playing(request, username):
    track = Visualizer(username).currently_playing_track()
    track_obj = {
        'error': 'no track currently playing'} if track is None else track
    return JsonResponse(track_obj)


def playingnext(request, username):
    vis = Visualizer(username)
    track = vis.wait_for_next_track()
    track_obj = {
        'error': 'no track currently playing'} if track is None else track
    return JsonResponse(track_obj)
