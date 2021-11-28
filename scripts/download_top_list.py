import requests
import pandas as pd
import re
from datetime import datetime

from connect import make_headers

country_dict = {
    'global': 'Global',
    'us': 'United_States',
    'gb': 'United_Kingdom',
    'au': 'Australia',
    'br': 'Brazil',
    'fr': 'France',
    'gr': 'Greece',
    'tr': 'Turkey',
    'id': 'Indonesia',
    'jp': 'Japan',
    'hk': 'Hong_Kong',
    'ru': 'Russian_Federation'
    }

# country_dict = {'global': 'Global'}

# Define headers
headers = make_headers()

def get_url_content(country_code, scope="top50"):
    """
    In URL: for top50, use /viral/. Else, use /regional/ to get top200
    """
    if scope == "top50":
        URL = f"https://spotifycharts.com/viral/{country_code}/daily/latest/download"
    else:
        URL = f"https://spotifycharts.com/regional/{country_code}/daily/latest/download"
    return requests.get(URL, headers=headers).content.splitlines()

def response_to_dict(response):
    keys = response[1].decode().split(',')
    keys = [k.replace('"', '') for k in keys]
    content = [r.decode().split(',') for r in response[2:]]
    list_of_contents = [list(z) for z in zip(*content)]
    return dict(zip(keys, list_of_contents))

def dict_to_df(D):
    df = pd.DataFrame(D)
    df["Track_id"] = df.URL.apply(lambda s: re.sub('.*/', '', s))
    return df

def get_top_lists(country_dict, scope="top50"):
    """
    Get top-lists for each country in country_dict
    """
    curr_date = datetime.today()
    for country_code, country_name in country_dict.items():
        print(f"Getting {country_name}...")
        response = get_url_content(country_code, scope)
        D = response_to_dict(response)
        df = dict_to_df(D)
        df['Country'] = country_name
        df['Date'] = curr_date
        df.to_csv(f"../data/top_lists/top_list_{country_name}.csv", index=False)

    return None

if __name__ == "__main__":

    get_top_lists(country_dict)

