# Data from https://www.albion-online-data.com/

import requests
import pprint

from typing import List

def list_to_url(data_url, tier: str, data: List[str], tier_prefix=False) -> str:
    for item in data:
        if tier_prefix:
            data_url += f"{tier}_{item},"
        else:
            data_url += f"{item},"
    return data_url

def translate_url(tiers: List[str], item_data: List[str], cities: List[str], qualities: List[str]) -> tuple[str, str, str]:
    data_url = ""
    for tier in tiers:
        data_url = list_to_url(data_url, tier=tier, data=item_data, tier_prefix=True)
    cities_url = ""
    for tier in tiers:
        cities_url = list_to_url(cities_url, tier=tier, data=cities)
    qualities_url = ""
    for tier in tiers:
        qualities_url = list_to_url(qualities_url, tier=tier, data=qualities)

    return data_url, cities_url, qualities_url

def get_timely_price(server='east', cities=['Lymhurst'], tiers=['T5'], qualities = ['1'], item_data=[]) -> List[dict]:
    data_url, cities_url, qualities_url = translate_url(tiers=tiers, item_data=item_data, cities=cities, qualities=qualities)
    try:
        url = f"https://{server}.albion-online-data.com/api/v2/stats/prices/{data_url}?locations={cities_url}&qualities={qualities_url}"
        print(url)
        r = requests.get(url)
        pprint.pprint(r.json())
        return r.json()
    except Exception as e:
        print (f"Error {e}")
    return []

# TODO: Using history data to calculate avg price
def get_history_price(server='east', cities=['Lymhurst'], tiers=['T5'], qualities = ['1'], item_data=[], time_scale=1, start_date = None, end_date = None) -> List[dict]:
    """
        time_scale: for hours
    """
    data_url, cities_url, qualities_url = translate_url(tiers=tiers, item_data=item_data, cities=cities, qualities=qualities)
    try:
        url = f"https://{server}.albion-online-data.com/api/v2/stats/history/{data_url}?date={start_date}&end_date={end_date}&locations={cities_url}&qualities=qualities={qualities_url}?time-scale={time_scale}"
        print(url)
        r = requests.get(url)
        pprint.pprint(r.json())
        return r.json()
    except Exception as e:
        print (f"Error {e}")
    return []

if __name__ == '__main__':
    get_timely_price()