import json
import uuid
import os
# comment
def dict_to_file(input: dict, fname: str) -> bool:
    fname += f"_{str(uuid.uuid1())[:3]}"
    with open(f"{fname}.json", 'w') as json_file:
        json.dump(input, json_file, indent=4)
        return True


def json_privates_loader():
    result = []
    for fname in filter(lambda x: x.endswith('.json'), os.listdir()):
        with open(fname) as infile:
            js = json.load(infile)
            result.append(js['private'])
    if not result:
        raise Exception('cant find private keys exitting')
    return result