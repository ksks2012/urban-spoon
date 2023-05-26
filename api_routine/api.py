# Data from https://www.albion-online-data.com/

import requests
import pprint

from typing import List

def list_to_url(data_url, tier: str, data: List[str], tier_prefix=False):
    for item in data:
        if tier_prefix:
            data_url += f"{tier}_{item},"
        else:
            data_url += f"{item},"
    return data_url

def get_price(server='east', cities=['Lymhurst'], tiers=['T5'], qualities = ['1'], data=[]):
    data_url = ""
    for tier in tiers:
        data_url = list_to_url(data_url, tier=tier, data=data, tier_prefix=True)
    cities_url = ""
    for tier in tiers:
        cities_url = list_to_url(cities_url, tier=tier, data=cities)
    qualities_url = ""
    for tier in tiers:
        qualities_url = list_to_url(qualities_url, tier=tier, data=qualities)

    try:
        url = f"https://{server}.albion-online-data.com/api/v2/stats/prices/{data_url}?locations={cities_url}&qualities={qualities_url}"
        print(url)
        r = requests.get(url)
        pprint.pprint(r.json())
        return r.json()
    except Exception as e:
        print (f"Error {e}")
    return []

if __name__ == '__main__':
    get_price()