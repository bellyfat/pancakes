import json
import uuid

# comment
def dict_to_file(input: dict, fname: str) -> bool:
    fname += f"_{str(uuid.uuid1())[:3]}"
    with open(f"{fname}.json", 'w') as json_file:
        json.dump(input, json_file, indent=4)
        return True