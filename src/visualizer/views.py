from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from spotipy.oauth2 import SpotifyOAuth, is_token_expired
from spotipy import Spotify
import uuid


def index(request):
    if not request.session.get('uuid'):
        request.session['uuid'] = str(uuid.uuid4())

    auth_manager = SpotifyOAuth(
        scope='user-read-currently-playing',
        show_dialog=True)
    if request.method == 'GET':
        if request.GET.get("code"):
            # Step 3. Being redirected from Spotify auth page
            request.session['token'] = auth_manager.get_access_token(
                code=request.GET.get("code"), check_cache=False)
            return redirect(index)

    if not request.session.get('token'):
        auth_url = auth_manager.get_authorize_url()
        context = {'auth_url': auth_url}
        return render(request, "visualizer/index.html", context)

    if is_token_expired(request.session.get('token')):
        request.session['token'] = auth_manager.refresh_access_token(
            request.session.get('token')['refresh_token'])

    spotify = Spotify(request.session.get('token')['access_token'])
    request.session['username'] = spotify.me()['id']
    if (not 'display-mode' in request.session.keys()):
        request.session['display-mode'] = 'mirror-side'
    if (not 'display-names' in request.session.keys()):
        request.session['display-names'] = 'no'
    context = {'username': request.session.get('username'), 'display_mode': request.session.get(
        'display-mode'), 'display_names': request.session.get('display-names')}
    return render(request, "visualizer/index.html", context)


def signout(request):
    request.session.flush()
    return redirect(index)


def visview(request, username):
    if not request.session.get('username'):
        return redirect(index)
    if username != request.session.get('username'):
        return redirect(visview, request.session['username'])
    auth_manager = SpotifyOAuth(scope='user-read-currently-playing')
    if (not request.session.get('token')) or auth_manager.is_token_expired(request.session.get('token')):
        return redirect(index)
    context = {'username': username, 'sessionid': request.session.get('uuid')}
    return render(request, "visualizer/vis.html", context)


def update_settings(request):
    request.session['display-mode'] = request.POST['display-mode']
    request.session['display-names'] = True if request.POST['display-names'] == 'yes' else False
    return redirect(index)
