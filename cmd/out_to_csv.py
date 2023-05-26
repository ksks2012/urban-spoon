import pprint
from api_routine.api import get_price
from utils.read_file import read_yaml
from utils import path


def main():
    worker_conf = read_yaml(path.WORKER_CONF)
    header = worker_conf.get('header', {})

    data = {}
    for key, value in worker_conf.items():
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
            if v['sell_price_min'] == 0:
                price = v['buy_price_max']
            elif v['buy_price_min'] == 0:
                price = v['sell_price_min']
            else:
                price = int((v['sell_price_min'] + v['buy_price_max']) / 2)
            tmp_data[v['item_id']] = price
        if key not in result_data:
            result_data[key] = tmp_data
        else:
            result_data[key].update(tmp_data)

    # data to rows
    for key, value in worker_conf.items():
        if key == 'header':
            continue
        print(f'{key}:')
        for tier in header.get('tier', []):
           for v in value:
                print(f"{result_data[key][f'{tier}_{v}']}")
        print('~~~~~~~~~~~~~\n')         

if __name__ == '__main__':
    main()