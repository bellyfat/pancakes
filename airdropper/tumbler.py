import time
import copy
import random
from utils import json_privates_loader
from web3 import Web3
from eth_account import Account


class Tumbler:
    chain_id = 97
    endpoint_uri = 'https://data-seed-prebsc-1-s1.binance.org:8545/'
    gasPrice = 20

    def __init__(self, privates: list):
        self.privates = privates
        self.web3 = Web3(Web3.HTTPProvider(type(self).endpoint_uri))
        if not self.web3.isConnected():
            raise Exception("Can't connect to endpoint")

    def transfer_value(self, addr_a: Account, addr_b: Account):
        gasCost = 21000
        gasPrice = self.web3.toWei(10, 'gwei')

        while True:
            mempool = self.web3.geth.txpool.content()
            if addr_a.address not in mempool['queued'] and addr_a.address not in mempool['queued']:
                break
            print('addr in mempool waiting')
            time.sleep(1)

        nonce = self.web3.eth.getTransactionCount(addr_a.address)
        balance =  self.web3.eth.get_balance(addr_a.address)
        balance -= gasCost * gasPrice

        tx = { 'nonce': nonce, 'chainId': type(self).chain_id, 'to': addr_b.address,
               'value': balance, 'gas': gasCost, 'gasPrice': gasPrice }
        if balance > 0:
            signed = self.web3.eth.account.sign_transaction(tx, addr_a.privateKey)
            hashed = self.web3.eth.send_raw_transaction(signed.rawTransaction)
            print(self.web3.toHex(hashed))
        else:
            print(f'not enough balance for {addr_a.address}')

if __name__ == '__main__':
    p = Tumbler(json_privates_loader())
    z = copy.deepcopy(p.privates)
    random.shuffle(z)
    a = Account.privateKeyToAccount(z.pop())
    while len(z) > 1:
        b = Account.privateKeyToAccount(z.pop())
        p.transfer_value(a,b)
        a = b