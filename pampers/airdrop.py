import os
import logging

from web3 import Web3
from eth_account import Account


from tx.builders import transfer
from tx.senders import sign_and_send, check_txpool
from utils.accounts import account_new, account_nonce


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



acc = Account.from_key(os.getenv('PRIVATE_KEY', 'takeitback'))
w3 = Web3(Web3.HTTPProvider(os.getenv('RPC', 'https://data-seed-prebsc-1-s1.binance.org:8545')))


def calculate_over_amount_wallets(amount: int = 30):
    '''spreads the available balance over a fixed mount of wallets'''
    balance = w3.eth.get_balance(acc.address)
    per_wallet = balance // amount
    return balance, per_wallet


def calculate_over_size_bag(amount: float = 0.1):
    '''amount is measured in ether/bnb so 0.01 bnb or 0.1 bnb'''
    balance = w3.eth.get_balance(acc.address)
    per_wallet = balance // w3.toWei(amount, 'ether')
    return balance, per_wallet




if __name__ == '__main__':
    amount_wallets = 50
    balance, per_wallet = calculate_over_amount_wallets(amount_wallets)
    nonce = check_txpool(w3, acc) 
    nonce = account_nonce(w3, acc) if nonce == None else nonce
    for i in range(0, amount_wallets):
        new_holder = account_new()
        txs = transfer(
            nonce=nonce,
            id=os.getenv('ID', '97'),
            to_address=new_holder.address,
            value=per_wallet
        )
        sign_and_send(w3, acc, txs)
        logging.warning('send the transaction with nonce %s of %s to %s', nonce, w3.fromWei(per_wallet, 'ether'), new_holder.address)
        nonce+=1

