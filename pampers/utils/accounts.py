import os
import secrets, logging
from eth_account import Account

from web3 import Web3
from web3.contract import Contract

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


def account_new() -> Account:
    return Account.create(secrets.token_hex(32))

def account_load(private_key: str) -> Account:
    return Account.from_key(private_key)

def account_balance_eth(w3: Web3, acc: Account):
    '''returns balance in wei'''
    return w3.eth.get_balance(acc.address)

def account_balance_contract(contract: Contract, acc: Account):
    '''returns balance in wei'''
    balance = contract.functions.balanceOf(acc.address).call()

def account_nonce(w3: Web3, account: Account):
    nonce = w3.eth.getTransactionCount(account.address)
    logger.debug('nonce: %s for account %s', nonce, account.address)
    return nonce