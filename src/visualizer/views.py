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
        return HttpResponse(f'<h2><a href="{auth_url}">Sign in</a></h2>')

    if is_token_expired(request.session.get('token')):
        request.session['token'] = auth_manager.refresh_access_token(
            request.session.get('token')['refresh_token'])

    spotify = Spotify(request.session.get('token')['access_token'])
    request.session['username'] = spotify.me()['id']
    return redirect(visview, request.session.get('username'))


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
