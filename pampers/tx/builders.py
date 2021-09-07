import json, os
import logging


logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
if os.getenv('DEBUG', 'True') == 'True':
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



from web3 import Web3

def tx(nonce, id, value) -> json:
    logging.debug('building tx with values nonce: %s, chain id: %s, value: %s', nonce, id, value)
    return { 'nonce': int(nonce),
             'chainId': int(id),
             'value':value,
             'gasPrice': Web3.toWei(os.getenv('GAS_PRICE', '10'), 'gwei') }

def swap(nonce, id, from_address, value) -> json:
    raw = tx(nonce, id, value)
    raw['from'] = from_address
    raw['gas'] = 250000
    return raw


def transfer(nonce, id, to_address, value) -> json:
    raw = tx(nonce, id, value)
    raw['to'] = to_address
    raw['gas'] = 21000
    raw['value'] = value - raw['gasPrice'] * 21000
    return raw
