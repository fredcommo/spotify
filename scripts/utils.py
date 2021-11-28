import requests
from connect import make_headers

headers = make_headers()

def get_spotify(API, Id):
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'
    r = requests.get(BASE_URL + API + Id, headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

