import pprint
import sys
from api_routine.api import get_price
from utils.read_file import read_yaml
from utils import path


def main(config_path=None):
    if config_path is None:
        config_path = path.WORKER_CONF
    conf_data = read_yaml(config_path)
    header = conf_data.get('header', {})

    data = {}
    for key, value in conf_data.items():
        if key == 'header':
            continue
        
        data[key] = get_price(server=header.get('server', ''), 
                                cities=header.get('cities', []), 
                                tiers=header.get('tier', []), 
                                qualities=header.get('qualities', []), 
                                data=value)
        
    pprint.pprint(data)

    # get prices
    result_data = {}
    for key, value in data.items():
        tmp_data = {}
        for i, v in enumerate(value):
            # TODO: price check
            if v['sell_price_min'] == 0 or v['buy_price_max'] == 0:
                price = 0
            else:
                price = int((v['sell_price_min'] + v['buy_price_max']) / 2)
            tmp_data[f"{v['city']} {v['item_id']}"] = price
        if key not in result_data:
            result_data[key] = tmp_data
        else:
            result_data[key].update(tmp_data)

    # data to rows
    for key, value in conf_data.items():
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
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()