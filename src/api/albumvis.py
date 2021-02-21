from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import urllib
from PIL import Image

from django.conf import settings
from .models import Album, Render


# def prune_track(track):
#     if track is not None:
#         return {'error': None,
#                 'id': track['item'***REMOVED***['id'***REMOVED***,
#                 'album': {
#                     'id': track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED***,
#                     'name': track['item'***REMOVED***['album'***REMOVED***['name'***REMOVED***},
#                 'name': track['item'***REMOVED***['name'***REMOVED***}
#     ***REMOVED***
#         return {'error': "no track"}


class Visualizer:
    def __init__(self, username):
        SCOPE = 'user-read-currently-playing'
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(scope=SCOPE, username=username))

    def currently_playing_track(self):
        track = self.sp.current_user_playing_track()
        return track

    # TODO: if track is None it should wait until newtrack is not None,
    # also it shouldn't return if track is different but from same album

    def wait_for_next_track(self):
        track = self.sp.current_user_playing_track()
        while(True):
            sleep(3)
            newtrack = self.sp.current_user_playing_track()
            if track is None:
                if newtrack is not None:
                    return newtrack
            ***REMOVED***
                if newtrack is not None:
                    if track['item'***REMOVED***['id'***REMOVED*** != newtrack['item'***REMOVED***['id'***REMOVED***:
                        return newtrack

    def get_album_path(self, track):
        raw_url = settings.MEDIA_URL + "raw/" + \
            track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED*** + '.jpg'
        if len(Album.objects.filter(uri=track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED***)) != 0:
            return raw_url

        raw_path = settings.MEDIA_ROOT + "/raw/" + \
            track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED*** + '.jpg'
        raw_img_url = track['item'***REMOVED***['album'***REMOVED***['images'***REMOVED***[0***REMOVED***['url'***REMOVED***
        urllib.request.urlretrieve(raw_img_url, raw_path)
        raw_img = Image.open(raw_path)
        if raw_img.mode == "L":  # if grayscale, convert to RGB
            raw_img = raw_img.convert("RGB")
            raw_img.save(raw_path, "PNG")
        alb = Album(uri=track['item'***REMOVED***['album'***REMOVED***['id'***REMOVED***,
                    artist_name="someone", album_name="someone", raw_image=raw_path, url=raw_url)
        alb.save()
        return raw_url
