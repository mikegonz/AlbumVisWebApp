from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


class Visualizer:
    def __init__(self, username):
        SCOPE = 'user-read-currently-playing'
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(scope=SCOPE, username=username))

    def currently_playing_track(self):
        track = self.sp.current_user_playing_track()
        if track is not None:
            return track
