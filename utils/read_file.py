import yaml
import pprint

from typing import Mapping

def read_yaml(filename: str) -> Mapping :
    data = {}
    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(e)
    pprint.pprint(data)
    return data

if __name__ == '__main__':
    read_yaml('./etc/worker.yaml')