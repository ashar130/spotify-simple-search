from . import spotify_search_result_item
# import spotify_search_result_item
import base64
import requests
from urllib.parse import urlencode


class SpotifyAPI():
    client_id = None
    client_secret = None
    access_token = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {'Authorization': f'Basic {client_creds_b64}'}

    def perform_auth(self):
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {'grant_type': 'client_credentials'}
        token_header = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_header)
        if r.status_code in range(200, 299):
            token_response_data = r.json()
            self.access_token = token_response_data['access_token']
            print("success")

    def get_artist_data(self, artist):
        try:
            name = artist['name']
            weblink = artist['external_urls']['spotify']
            image = artist['images'][0]
            genres = artist['genres']
            followers = artist['followers']['total']
            artist_data = spotify_search_result_item.Artist(
                name, weblink, image, genres, followers)
        except:
            # print('Error')
            return False
        return artist_data

    def get_artists(self, data):
        artists_search_result = []
        for artist in data['artists']['items']:
            artist_data = self.get_artist_data(artist)
            if artist_data == False:
                continue
            else:
                artists_search_result.append(artist_data)
        return artists_search_result

    def get_album_data(self, album):
        try:
            name = album['name']
            artist = album['artists'][0]['name']
            weblink = album['external_urls']['spotify']
            image = album['images'][0]
            release_date = album['release_date']
            album_data = spotify_search_result_item.Album(
                name, weblink, image, artist, release_date)
        except:
            return False
        return album_data

    def get_albums(self, data):
        albums_search_result = []
        for album in data['albums']['items']:
            album_data = self.get_album_data(album)
            if album_data == False:
                continue
            else:
                albums_search_result.append(album_data)
        return albums_search_result

    def get_track_data(self, track):
        try:
            name = track['name']
            artist = track['artists'][0]['name']
            weblink = track['external_urls']['spotify']
            image = track['album']['images'][0]
            album = track['album']['name']
            release_date = track['album']['release_date']
            track_data = spotify_search_result_item.Track(name, weblink, image,
                                                          artist, album, release_date)
        except:
            return False
        return track_data

    def get_tracks(self, data):
        tracks_search_result = []
        for track in data['tracks']['items']:
            track_data = self.get_track_data(track)
            if track_data == False:
                continue
            else:
                tracks_search_result.append(track_data)
        return tracks_search_result

    def base_search(self, query, search_type):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        query = " ".join([f"{k}:{v}" for k, v in query.items()])
        endpoint = 'https://api.spotify.com/v1/search'
        query_params = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f'{endpoint}?{query_params}'
        r = requests.get(lookup_url, headers=headers)
        return r.json()

    def get_search_type(self, query):
        if query['track'] is not None:
            search_type = 'track'
        elif query['album'] is not None:
            search_type = 'album'
        else:
            search_type = 'artist'
        return search_type

    def format_query(self, query):
        formatted_query = {k: v for k, v in query.items() if v is not None}
        return formatted_query

    def search(self, query):
        search_type = self.get_search_type(query)
        query = self.format_query(query)
        data = self.base_search(query, search_type)
        if search_type == 'artist':
            search_result = self.get_artists(data)
        elif search_type == 'album':
            search_result = self.get_albums(data)
        else:
            search_result = self.get_tracks(data)
        # print(search_result)
        return search_result
