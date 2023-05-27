import json
import os
import pprint

from utils import path
from utils import read_file

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

if __name__ == '__main__':
    # test_worker_price()
    test_multi_cities()