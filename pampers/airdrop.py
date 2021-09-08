import sys
import os
import math
from pathlib import Path

try:
    from pampers import w3, acc, log
except Exception as e:
    sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__))).parents[0]))
    from pampers import w3, acc, log

from tx.builders import transfer
from tx.senders import sign_and_send, check_txpool
from utils.accounts import account_new, account_nonce

def calculate_over_amount_wallets(amount: int = 30):
    '''spreads the available balance over a fixed mount of wallets'''
    balance = w3.eth.get_balance(acc.address)
    if balance == 0:
        raise Exception('airdropping wallet has no balance')
    per_wallet = balance // amount
    return per_wallet


def calculate_over_size_bag(amount: float = 0.1):
    '''amount is measured in ether/bnb so 0.01 bnb or 0.1 bnb'''
    balance = w3.eth.get_balance(acc.address)
    if balance == 0:
        raise Exception('airdropping wallet has no balance')
    amount = w3.toWei(amount, 'ether')
    amount_wallets = balance / amount
    return amount, math.floor(amount_wallets)

if __name__ == '__main__':
    bag_size = 0.001
    per_wallet, amount_wallets = calculate_over_size_bag(bag_size)
    nonce = check_txpool() 
    nonce = account_nonce(acc) if nonce == None else nonce
    for i in range(0, amount_wallets):
        log.info('airdrop %s', i)
        log.info('  airdrop:  %s BNB', w3.fromWei(per_wallet, 'ether'))
        new_holder = account_new()
        txs = transfer(
            nonce=nonce,
            id=os.getenv('ID', '97'),
            to_address=new_holder.address,
            value=per_wallet
        )
        sign_and_send(txs, check_mempool=False)
        nonce+=1

