import sys
import os

import secrets

from pathlib import Path

from eth_account import Account

from web3.contract import Contract

try:
    from pampers import w3, acc, log
except Exception as e:
    sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__))).parents[1]))
    from pampers import w3, acc, log


def account_new() -> Account:
    account = Account.create(secrets.token_hex(32))
    priv, pub = account.privateKey.hex(), account.address
    log.info('  private:  %s', priv)
    log.info('  public:   %s', pub)
    return account

def account_load(private_key: str) -> Account:
    log.debug('loaded account with existing private key')
    return Account.from_key(private_key)

def account_balance_eth(account: Account):
    '''returns balance in wei'''
    return w3.eth.get_balance(account.address)

def account_balance_contract(contract: Contract, account: Account):
    '''returns balance in wei'''
    balance = contract.functions.balanceOf(account.address).call()
    log.debug('balance is %s for account %s', balance, account.address)
    return balance


def account_nonce(account: Account):
    nonce = w3.eth.getTransactionCount(account.address)
    log.debug('nonce is %s for account %s', nonce, account.address)
    return nonce

if __name__ == '__main__':
    nonce = account_nonce(acc)