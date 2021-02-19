from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from time import sleep


class Visualizer:
    def __init__(self, username):
        SCOPE = 'user-read-currently-playing'
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(scope=SCOPE, username=username))

    def currently_playing_track(self):
        track = self.sp.current_user_playing_track()
        if track is not None:
            return track

    # TODO: if track is None it should wait until newtrack is not None,
    # also it shouldn't return if track is different but from same album
    def wait_for_next_track(self):
        track = self.sp.current_user_playing_track()
        while(track):
            sleep(3)
            newtrack = self.sp.current_user_playing_track()
            if track['item'***REMOVED***['id'***REMOVED*** != newtrack['item'***REMOVED***['id'***REMOVED***:
                return newtrack
        if track is None:
            return None
