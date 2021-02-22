from .albumvis import Visualizer
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def index(request):
    track_name = 'no username provided'
    context = {'track': track_name, 'js': {'path': 'uhoh.jpg'}}
    return render(request, 'api/index.html', context)


def playing(request, username):
    vis = Visualizer(username)
    track = vis.currently_playing_track()
    if track is None:
        return JsonResponse({
            'error': 'no track currently playing'})
    img_path = vis.get_render_path(track, "solid")
    response = {'path': img_path}
    return JsonResponse(response)


def playingnext(request, username):
    vis = Visualizer(username)
    track = vis.wait_for_next_track()
    if track is None:
        return JsonResponse({
            'error': 'no track currently playing'})
    img_path = vis.get_render_path(track, "solid")
    response = {'path': img_path}
    return JsonResponse(response)
