# import requests
import pandas as pd
# import re
import glob
import os
from datetime import datetime

from utils import get_spotify

# from connect import make_headers

# headers = make_headers()

# def get_track_info(track_id):
#     # base URL of all Spotify API endpoints
#     BASE_URL = 'https://api.spotify.com/v1/'
#     API = 'audio-features/'
#     r = requests.get(BASE_URL + API + track_id, headers=headers)
#     return pd.DataFrame(r.json(), index=[track_id])

def get_track_info_by_country(filename):

    def _get_track_info(API, track_id):
        r = get_spotify(API, track_id)
        return pd.DataFrame(r, index=[track_id])

    # This may fail: include retry!
    print(f"Getting tracks info for {os.path.basename(filename)}...", end = " ")
    df = pd.read_csv(filename)

    API = 'audio-features/'

    tracks_info = [_get_track_info(API, track_id) for track_id in df.Track_id]
    tracks_info = pd.concat(tracks_info).reset_index(drop=False)
    tracks_info.rename(columns={'index':'Track_id'}, inplace=True)
    tracks_info = df.merge(tracks_info, on="Track_id")
    print("Done!")

    return tracks_info

def get_all_tracks_info():
    files_list = glob.glob('../data/top_lists/*')
    all_tracks = [get_track_info_by_country(filename) for filename in files_list]
    return pd.concat(all_tracks)

if __name__ == "__main__":
    curr_date = datetime.today()
    all_tracks = get_all_tracks_info()
    all_tracks["track_info_Date"] = curr_date
    short_date = curr_date.strftime("%Y%m%d")
    all_tracks.to_csv(f"../data/tracks_infos/tracks_info_{short_date}.csv", index=False)
