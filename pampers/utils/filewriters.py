import json
import uuid
import os
import secrets
from eth_account import Account

# comment
def dict_to_file(input: dict, fname: str) -> bool:
    fname += f"_{str(uuid.uuid1())[:5]}"
    with open(f"{fname}.json", 'w') as json_file:
        json.dump(input, json_file, indent=4)
        return True


def json_loader(dir: str):
    result = []
    for fname in filter(lambda x: x.endswith('.json'), os.listdir()):
        with open(fname) as infile:
            js = json.load(infile)
            if js['private'] not in result:
                result.append(js['private'])
    if not result:
        raise Exception('cant find private keys exitting')
    return result