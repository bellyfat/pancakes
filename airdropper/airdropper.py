
import secrets
import math, time
import json
from utils import dict_to_file

from web3 import Web3
from eth_account import Account

from chains import bsc_testnet as chain

PRIVATE_KEY = 'b71210ec086f6b855c424fd65a945813f0b9f7866df559f49e1efa89bd958605'

airdrop = {'seed_size' : 0.14, 'drop_size': 4 }

class Airdropper:
    gas: int = None
    gasPrice: int = None
    amount_wallets: int = None
    nonce: int = None
    connections: list = []
    disconnected: list = []

    def __init__(self,  chain, signer, airdrop):
        self.chain = chain
        self.signer = signer
        self.airdrop = airdrop
        self.gas = 200000
        self.w3 = None
        self.connect()
        if type(self).amount_wallets == None:
            self.calculate_airdrop()
            self.set_gas()

    def set_gas(self, increase_gas = False, increase_price = False):
        if increase_price:
            type(self).gasPrice = math.floor(type(self).gasPrice * 1.25)
        else:
            type(self).gasPrice = self.chain.get('gasPrice')
        if increase_gas:
            type(self).gas = math.floor(self.gas * 1.25)
        else:
            type(self).gas = self.gas

    def fetch_nonce(self):
        nonce = self.w3.eth.getTransactionCount(self.signer.address)
        type(self).nonce = nonce
        return type(self).nonce

    def calculate_airdrop(self):
        balance = self.w3.eth.get_balance(self.signer.address)
        size = self.airdrop.get('drop_size')
        if balance >= self.w3.toWei(size, 'Ether'):
            amount = math.floor(self.w3.toWei(size, 'Ether') / self.w3.toWei(self.airdrop.get('seed_size'), 'Ether'))
            type(self).amount_wallets = amount

    def connect(self, method: str = 'http'):
        for uri in filter(lambda x: x not in type(self).connections, self.chain.get(method)):
            if method == 'http':
                w3 = Web3(Web3.HTTPProvider(uri))
            elif method == 'wss':
                w3 = Web3(Web3.WebsocketProvider(uri))
            if w3.isConnected():
                type(self).connections.append(w3.provider.endpoint_uri)
                self.w3 = w3
                type(self).nonce = self.w3.eth.getTransactionCount(self.signer.address)
                break

    def build_tx(self, address):
        return { 'nonce': type(self).nonce,
                'chainId': self.chain.get('chainid'),
                'to': address,
                'value': self.w3.toWei(self.airdrop.get('seed_size'), 'Ether'),
                'gas': type(self).gas,
                'gasPrice': self.w3.toWei(type(self).gasPrice, 'gwei') }

    def send_transaction(self, to: Account):
        address = to.address
        mempool = self.w3.geth.txpool.content()
        while True:
            if self.signer.address not in mempool['queued'] and self.signer.address not in mempool['pending']:
                break
            time.sleep(1)
            mempool = self.w3.geth.txpool.content()
        while True:
            try:
                tx = self.build_tx(address)
                signed = self.w3.eth.account.sign_transaction(tx, self.signer.privateKey)
                hashed = self.w3.eth.send_raw_transaction(signed.rawTransaction)               
                dict_to_file({'hash': f"{self.chain.get('explorer')}{self.w3.toHex(hashed)}", 
                              'address': address, 
                              'private': to.privateKey.hex()}, 
                              'tumble_0')
                type(self).nonce += 1
                break
            except Exception as e:
                err = e.args[0]
                if err['message'] == 'transaction underpriced':
                    print(f'tx underpriced increasing gas from {type(self).gasPrice} with 25%')
                    self.set_gas(increase_price = True)
                    time.sleep(1)
                elif 'already known' in err['message']:
                    print(err)
                    time.sleep(3)
                elif 'nonce too low' in err['message']:
                    type(self).nonce += 1
                else:
                    print('fatal error happened. last known transaction was')
                    print(to.privateKey.hex())
                    print(to.address)
                    print(e)
                    exit()


if __name__ == '__main__':
    signer = Account.privateKeyToAccount(PRIVATE_KEY)
    dropper = Airdropper(chain, signer, airdrop)
    print(f'airdropping on {dropper.amount_wallets}')
    for i in range(0, dropper.amount_wallets):
        dropper.send_transaction(to = Account.create(secrets.token_hex(32)))