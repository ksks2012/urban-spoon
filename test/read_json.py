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

if __name__ == '__main__':
    json_data = read_json('price.json')

    result_data = {}
    for key, value in json_data.items():
        tmp_data = {}
        for i, v in enumerate(value):
            price = max(v['sell_price_min'], v['buy_price_max'])
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