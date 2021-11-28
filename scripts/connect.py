import requests
import json

creds_file = ".credentials.json"
with open(creds_file) as json_file:
    creds = json.load(json_file)

def make_headers():
    client_id = creds["spotity"]["client_id"]
    client_secret = creds["spotity"]["client_secret"]

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    # Define headers
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

    return headers