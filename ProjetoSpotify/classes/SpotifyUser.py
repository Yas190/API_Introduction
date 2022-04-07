import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

class SpotifyUser:

    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def get_redirect_uri(self):
        return self.redirect_uri

    def get_scope(self):
        return self.scope

    def set_client_id(self, client_id, inplace=False):
        if inplace:
            self.client_id = client_id
        else:
            return SpotifyUser(client_id, self.client_secret, self.redirect_uri, self.scope)

    def set_client_secret(self, client_secret, inplace=False):
        if inplace:
            self.client_secret = client_secret
        else:
            return SpotifyUser(self.client_id, client_secret, self.redirect_uri, self.scope)

    def set_redirect_uri(self, redirect_uri, inplace=False):
        if inplace:
            self.redirect_uri = redirect_uri
        else:
            return SpotifyUser(self.client_id, self.client_secret, redirect_uri, self.scope)

    def set_scope(self, scope, inplace=False):
        if inplace:
            self.scope = scope
        else:
            return SpotifyUser(self.client_id, self.client_secret, self.redirect_uri, scope)

    def _top_tracks(self):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(self.client_id, self.client_secret, self.redirect_uri, self.scope))
        ranges = ['short_term', 'medium_term', 'long_term']

        df_top_tracks = pd.DataFrame(columns=['POSICAO', 'MUSICA', 'ARTISTAS', 'DURAÇAO_EM_MS', 'PERIODO'])

        for sp_range in ranges:
            results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
            for i, item in enumerate(results['items']):

                track = pd.DataFrame({
                    'POSICAO': i,
                    'MUSICA': item['name'],
                    'DURAÇAO_EM_MS': item['duration_ms'],
                    'ARTISTAS': [artista['name'] for artista in item['artists']],
                    'PERIODO': sp_range
                })

                df_top_tracks = pd.concat([df_top_tracks, track], ignore_index=True)

        print(df_top_tracks.to_string())



    def get_top_tracks(self):
        print(self._top_tracks())
