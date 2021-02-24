from .albumvis import Visualizer
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings

from visualizer.views import index as visindex

from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

caches_folder = '.spotify_caches/'


def session_cache_path(session):
    return caches_folder + session.get('uuid') + ".cache"


def index(request):
    track_name = 'no username provided'
    context = {'track': track_name, 'js': {'path': 'uhoh.jpg'}}
    return render(request, 'api/index.html', context)


def get_track(request, username, isFirst):
    auth_manager = SpotifyOAuth(
        scope='user-read-currently-playing', cache_path=session_cache_path(request.session))
    spotify = Spotify(auth_manager=auth_manager)
    vis = Visualizer(username, spotify)
    track = vis.currently_playing_track() if isFirst else vis.wait_for_next_track()
    if track is None or track['item'] is None:
        return JsonResponse({
            'error': 'no track currently playing',
            'path': settings.STATIC_URL + "uhoh.jpg"})
    img_path = vis.get_render_path(track, "mirror-side")
    response = {'path': img_path}
    return JsonResponse(response)


def playing(request, username):
    return get_track(request, username, True)


def playingnext(request, username):
    return get_track(request, username, False)
