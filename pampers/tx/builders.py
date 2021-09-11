import json
import time, math
from pampers import log, CHAIN
from web3 import Web3

def tx(nonce, value) -> json:
    log.warning('building tx with values nonce: %s, chain id: %s, value: %s', nonce,CHAIN.get('ID'), value)
    return { 'nonce': int(nonce),
             'value': value,
             'chainId': int(CHAIN.get('ID')),
             'gasPrice': Web3.toWei(CHAIN.get('GAS_PRICE'), 'gwei') }

def swap(nonce, to_address, value) -> json:
    raw = tx(nonce, value)
    raw['from'] = to_address
    raw['gas'] = 250000
    tax = math.floor(raw['gasPrice'] * raw['gas']) * 3
    raw['value'] = value - tax
    return raw


def transfer(nonce, to_address, value) -> json:
    raw = tx(nonce, value)
    log.debug('taxing transaction and added metadata %s', raw)
    raw['to'] = to_address
    raw['gas'] = 21000
    tax = raw['gasPrice'] * raw['gas']
    raw['value'] = value - tax
    if raw['value'] < 0:
        raise Exception('the amount you want to send is less than gas fee. Aborting')
    log.debug('taxed transaction %s', raw)
    return raw
