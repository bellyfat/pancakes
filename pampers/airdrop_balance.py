import sys
import os
import math
import time
import csv
from pathlib import Path

try:
    from pampers import w3, acc, log
except Exception as e:
    sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__))).parents[0]))
    from pampers import w3, acc, log

from tx.builders import transfer
from tx.senders import sign_and_send, check_txpool
from utils.accounts import account_new, account_nonce


def calculate_amount_wallets(amount: float = 0.1):
    '''amount is measured in ether/bnb so 0.01 bnb or 0.1 bnb. returns amount of wallets to airdrop. Doesn't include gas fees'''
    balance = w3.eth.get_balance(acc.address)
    if balance == 0:
        raise Exception('airdropping wallet has no balance')
    amount_wallets = balance / w3.toWei(amount, 'ether')
    return amount_wallets


if __name__ == '__main__':
    per_wallet = 0.001
    amount_wallets = calculate_amount_wallets(per_wallet)
    nonce = check_txpool() 
    nonce = account_nonce(acc) if nonce == None else nonce
    for i in range(0, amount_wallets):
        log.info('airdrop %s', i)
        log.info('  airdrop:  %s BNB', per_wallet)
        new_holder = account_new()
        txs = transfer(
            nonce=nonce,
            id=os.getenv('ID', '97'),
            to_address=new_holder.address,
            value=w3.toWei(per_wallet)
        )
        sign_and_send(txs, check_mempool=False)
        nonce+=1

