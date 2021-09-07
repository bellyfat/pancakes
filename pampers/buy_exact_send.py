import os

from contract.helpers import loadRouter
from web3 import Web3

rpc = os.getenv('RPC', 'https://data-seed-prebsc-1-s1.binance.org:8545')
router = os.getenv('ROUTER', '0xD99D1c33F9fC3444f8101754aBC46c52416550D1')
w3 = Web3(Web3.HTTPProvider(rpc))
contract = loadRouter(w3, router)

