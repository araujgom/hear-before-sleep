import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from models import Album, SpotifyAlbum

class SpotifyService:
    def __init__(self):
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        ))

    def get_spotify_data(self, album: Album) -> SpotifyAlbum:
        query = f"album:{album.album_title} artist:{album.artist_name}"
        results = self.spotify.search(query, type='album', limit=1)

        if results['albums']['items']:
            spotify_album = results['albums']['items'][0]
            return SpotifyAlbum(
                album_title=album.album_title,
                artist_name=album.artist_name,
                album_description=album.album_description,
                spotify_url=spotify_album['external_urls']['spotify']
            )
        return None