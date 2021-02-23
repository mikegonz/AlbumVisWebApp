from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
import uuid

caches_folder = '.spotify_caches/'


def session_cache_path(session):
    return caches_folder + session.get('uuid') + ".cache"


def indasdfex(request):
    # if request.session.get('username'):
    #     return redirect(visview, request.session.get('username'))
    return redirect(index)
    # return render(request, "visualizer/index.html")


def index(request):
    if not request.session.get('uuid'):
        request.session['uuid'] = str(uuid.uuid4())

    auth_manager = SpotifyOAuth(
        scope='user-read-currently-playing',
        cache_path=session_cache_path(request.session),
        show_dialog=True)
    if request.method == 'GET':
        print('getting!')
        if request.GET.get("code"):
            # Step 3. Being redirected from Spotify auth page
            auth_manager.get_access_token(request.GET.get("code"))
            return redirect(index)

    if not auth_manager.get_cached_token():
        auth_url = auth_manager.get_authorize_url()
        return HttpResponse(f'<h2><a href="{auth_url}">Sign in</a></h2>')

    spotify = Spotify(auth_manager=auth_manager)
    request.session['username'] = spotify.me()['id']
    request.session['token'] = auth_manager.get_cached_token()
    return redirect(visview, request.session.get('username'))


def visview(request, username):
    context = {'username': username, 'sessionid': request.session.get('uuid')}
    return render(request, "visualizer/vis.html", context)
