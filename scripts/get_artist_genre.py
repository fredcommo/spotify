# import requests
import pandas as pd
# import re
import glob
# import os
from datetime import datetime

from utils import get_spotify


def get_track_popularity(track_info):
    return track_info['popularity']

def get_artist_id(track_info):
    artist = track_info['album']['artists'][0]
    return artist['name'], artist['id']


def get_artist_info(track_id):
    """
    Get artist name, artist id, track popularity and artist genres from a track_id

    Args:
        track_id (str): a track id

    Returns:
        A data frame with:
            - the artist name (str)
            - the artist id (str)
            - the track popularity (int form 0 to 100)
            - the artist genres (str)
    """

    # track_info = get_track_info_from_trackid(track_id)
    track_info = get_spotify('tracks/', track_id)
    if not track_info:
        return None

    popularity = get_track_popularity(track_info)
    artist_name, artist_id = get_artist_id(track_info)
    artist_info = get_spotify('artists/', artist_id)
    if not artist_info:
        genres = None
    else:
        genres = "|".join(artist_info['genres'])

    D = {
        'Artist_name': artist_name,
        'Artist_id': artist_id,
        'Track_popularity': popularity,
        'Artist_genres': genres
        }
    
    return pd.DataFrame(D, index=[track_id]).reset_index(drop=False)

def get_all_artists_infos():
    curr_date = datetime.today().strftime("%Y%m%d")
    track_file = glob.glob(f"../data/tracks_infos/*{curr_date}.csv")[0]
    df = pd.read_csv(track_file)
    track_ids = df.Track_id.unique()

    artists = [get_artist_info(_id) for _id in track_ids]
    artists = pd.concat(artists)
    artists.rename(columns={'index':'Track_id'}, inplace=True)

    artists.to_csv(f"../data/artists_info/artists_info_{curr_date}.csv", index=False)

    return None

    
if __name__ == "__main__":
    # track_id = "35mvY5S1H3J2QZyna3TFe0"
    # print(get_artist_info(track_id))
    get_all_artists_infos()