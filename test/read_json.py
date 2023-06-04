import json
import os
import pprint

from api_routine.api import get_history_price
from utils import path
from utils import read_file
from utils.read_file import read_yaml

def read_json(filename):
    data = {}
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        data = json.load(f)

    pprint.pprint(data)
    return data

def test_worker_price():
    json_data = read_json('price.json')

    result_data = {}
    for key, value in json_data.items():
        tmp_data = {}
        for i, v in enumerate(value):
            if v['sell_price_min'] == 0 or v['buy_price_max'] == 0:
                price = 0
            else:
                price = int((v['sell_price_min'] + v['buy_price_max']) / 2)
            tmp_data[v['item_id']] = price
        if key not in result_data:
            result_data[key] = tmp_data
        else:
            result_data[key].update(tmp_data)

    # pprint.pprint(result_data)

    worker_conf = read_file.read_yaml(path.WORKER_CONF)
    header = worker_conf.get('header', {})
    for key, value in worker_conf.items():
        if key == 'header':
            continue
        print(f'{key}:')
        for tier in header.get('tier', []):
           for v in value:
                print(f"{result_data[key][f'{tier}_{v}']}")
        print('~~~~~~~~~~~~~\n')         

def test_multi_cities():
    json_data = read_json('multi_cities.json')

    result_data = {}
    for key, value in json_data.items():
        tmp_data = {}
        for i, v in enumerate(value):
            if v['sell_price_min'] == 0 or v['buy_price_max'] == 0:
                price = 0
            else:
                price = int((v['sell_price_min'] + v['buy_price_max']) / 2)
            tmp_data[f"{v['city']} {v['item_id']}"] = price
        if key not in result_data:
            result_data[key] = tmp_data
        else:
            result_data[key].update(tmp_data)

    pprint.pprint(result_data)

    conf = read_file.read_yaml(path.ROCK_CONF)
    header = conf.get('header', {})
    for key, value in conf.items():
        if key == 'header':
            continue
        print(f'{key}:')
        for city in header.get('cities', []):
            print(f'\n{city}:')
            for tier in header.get('tier', []):
                for v in value:     
                    print(f"{result_data[key][f'{city} {tier}_{v}']}")
        print('~~~~~~~~~~~~~\n')         

def test_history_price():
    conf_data = read_yaml("./etc/history_price.yaml")
    header = conf_data.get('header', {})

    data = {}
    from time import gmtime, strftime
    strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    for key, value in conf_data.items():
        if key == 'header':
            continue
        
        data[key] = get_history_price(server=header.get('server', ''), 
                                cities=header.get('cities', []), 
                                tiers=header.get('tier', []), 
                                qualities=header.get('qualities', []), 
                                item_data=value,
                                time_scale=1,
                                start_date="6-2-2023",
                                end_date="6-3-2023",)

if __name__ == '__main__':
    # test_worker_price()
    # test_multi_cities()
    test_history_price()