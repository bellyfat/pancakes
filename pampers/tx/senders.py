import json
import logging
import os
import time

from eth_account import Account
from web3 import Web3


from collections import namedtuple


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


def connect_rpc(rpc: str = os.getenv('RPC', 'https://data-seed-prebsc-1-s1.binance.org:8545')):
    w3 = Web3(Web3.HTTPProvider(rpc))
    if w3.isConnected():
        logger.debug('connected to rpc endpoint: %s', rpc)
        return w3
    logger.critical('cant connect to rpc endpoint... exitting (%s)', rpc)
    raise Exception('rpc endpoint unavailable')

def check_txpool(w3: Web3, acc: Account):
    '''cancels transactions that are not yet in a block'''
    mempool = w3.geth.txpool.content()
    if acc.address in mempool['pending']:
        logging.warning('address found in mempool. Adding to nonce')
        if acc.address not in mempool['queued']:
            return 1 + max(int(x) for x in mempool['pending'][acc.address])
    if acc.address in mempool['queued']:
        logging.warning('nonce found in queue overriding it')
        return 1 + max(int(x) for x in mempool['queued'][acc.address])

def sign_and_send(w3: Web3, from_acc: Account, tx: json, check_mempool=False):
    if check_mempool:
        tx['nonce'] = check_txpool(w3, from_acc)
    signed_tx = w3.eth.account.sign_transaction(tx, from_acc.privateKey)
    logging.info('transaction signed succesfully')
    try:
        hashed_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        time.sleep(0.1)
        logging.info('transaction succesfully made %s', w3.toHex(hashed_tx))
        return w3.toHex(hashed_tx)           
    except Exception as e:
        logging.critical('something bad happened during transaction sending. Error: %s', e.args[0]['message'])
        logging.critical(tx)
        raise Exception('critical error')


if __name__ == '__main__':
    w3 = connect_rpc()