import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .player import Player

class SpotifyPlayer(Player):
    def __init__(self):
        self.client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_ID"), client_secret=os.getenv("SPOTIFY_SECRET"))
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def play(self, track_id):
        track_info = self.sp.track(track_id)
        if not track_info:
            print("No track found.")
            return None
        else:
            track_name = track_info['name']
            artist_name = track_info['artists'][0]['name']
            return artist_name + " " + track_name
