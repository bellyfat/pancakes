import json
import time
import os,sys
from pathlib import Path
from web3 import Account
try:
    from pampers import w3, log, acc, CHAIN
except Exception as e:
    sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__))).parents[1]))
    from pampers import w3, log, acc, CHAIN


def check_txpool():
    '''cancels transactions that are not yet in a block'''
    mempool = w3.geth.txpool.content()
    if acc.address in mempool['pending']:
        log.warning('address found in mempool. Adding to nonce')
        if acc.address not in mempool['queued']:
            return 1 + max(int(x) for x in mempool['pending'][acc.address])
    if acc.address in mempool['queued']:
        log.warning('nonce found in queue overriding it')
        return 1 + max(int(x) for x in mempool['queued'][acc.address])

def sign_and_send(tx: json, acc: Account, check_mempool=False):
    if check_mempool:
        tx['nonce'] = check_txpool()
    try:
        signed_tx = w3.eth.account.sign_transaction(tx, acc.privateKey)
        log.debug('transaction signed succesfully')
        hashed_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(hashed_tx)
        log.debug('transaction succesfully made %s', w3.toHex(hashed_tx))
        log.info('%s/tx/%s', CHAIN.get('EXPLORER'), w3.toHex(hashed_tx))
        return w3.toHex(hashed_tx)           
    except Exception as e:
        log.critical('something bad happened during transaction sending. Error: %s', e)
        log.critical(tx)
        raise Exception('critical error')
