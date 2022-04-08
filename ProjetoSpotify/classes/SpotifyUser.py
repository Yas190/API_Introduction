import spotipy # importando a biblioteca para acesso a API do Spotify
from spotipy.oauth2 import SpotifyOAuth # importando a biblioteca para autenticação no acesso a API
import pandas as pd # biblioteca pandas para a manipulação de dados
from google.cloud import bigquery # importando biblioteca para udo de dados do BigQuery

class SpotifyUser: # criando a classe SpotifyUser com atributos necessários

    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id # autenticação
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope # o que será buscado

    def get_client_id(self): # métodos get
        return self.client_id

    def get_client_secret(self):
        return self.client_secret

    def get_redirect_uri(self):
        return self.redirect_uri

    def get_scope(self):
        return self.scope

    def set_client_id(self, client_id, inplace=False): # métodos set
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

    def _top_tracks(self): # método estático para coletar dados das músicas mais ouvidas
        # variável para autenticação no acesso a API usando informações fornecidas no arquivo main.py
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(self.client_id, self.client_secret, self.redirect_uri, self.scope))
        # variável com lista dos períodos de tempo relacionados aos dados desejados
        ranges = ['short_term', 'medium_term', 'long_term']
        # criação do DataFrame vazio
        df_top_tracks = pd.DataFrame(columns=['POSICAO', 'MUSICA', 'ARTISTAS', 'DURAÇAO_EM_MS', 'PERIODO'])
        # loop para a coleta dos dados
        for sp_range in ranges:
            # método do spotipy, especificando o período e o limite de músicas)
            results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
            for i, item in enumerate(results['items']): # buscando as músicas na lista 'items' contando com a posição
                # inserindo os dados do loop em um novo DataFrame
                track = pd.DataFrame({
                    'POSICAO': i,
                    'MUSICA': item['name'],
                    'DURACAO_EM_MS': item['duration_ms'],
                    'ARTISTAS': [artista['name'] for artista in item['artists']],
                    'PERIODO': sp_range
                })
                # concatenando DataFrame vazio com novo DataFrame
                df_top_tracks = pd.concat([df_top_tracks, track], ignore_index=True)

        print(df_top_tracks.to_string())
        # fase de envio do DataFrame para o BiqQuery. Construindo um objeto cliente
        client = bigquery.Client()
        job_config = bigquery.LoadJobConfig(
            # estabelecendo esquema parcial da tabela, inserindo os tipos de dados das colunas
            schema=[
                bigquery.SchemaField('POSICAO', bigquery.enums.SqlTypeNames.INT64),
                bigquery.SchemaField('MUSICA', bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField('DURACAO_EM_MS', bigquery.enums.SqlTypeNames.INT64),
                bigquery.SchemaField('ARTISTAS', bigquery.enums.SqlTypeNames.STRING),
                bigquery.SchemaField('PERIODO', bigquery.enums.SqlTypeNames.STRING),
            ],
            # BigQuery substitui os dados da tabela já existente usando o esquema
            write_disposition="WRITE_TRUNCATE",
        )
        # API request
        job = client.load_table_from_dataframe(df_top_tracks, 'dynamic-market-346321.spotify.yasmin_cezere_pires',
                                               job_config=job_config
                                               )
        job.result()
        # API request
        table = client.get_table('dynamic-market-346321.spotify.yasmin_cezere_pires')
        print( f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {'dynamic-market-346321.spotify.yasmin_cezere_pires'}")
    # chamando método estático
    def get_top_tracks(self):
        print(self._top_tracks())
