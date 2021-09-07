import os
import json

from pathlib import Path
from web3 import Web3

abi_path = Path(os.path.dirname(os.path.realpath(__file__)))

def loadContract(w3: Web3, abi_json: str, address: str):
    address = Web3.toChecksumAddress(address)
    abi = json.load(open(abi_path.joinpath(abi_json), 'r'))['abi']
    contract_instance = w3.eth.contract(address=address, abi=abi)
    return contract_instance


def loadFactory(w3: Web3, factory_address: str):
    return loadContract(w3, 'IUniswapV2Factory.json', factory_address)


def loadRouter(w3: Web3, router_address: str):
    return loadContract(w3, 'IUniswapV2Router.json', router_address)


def loadToken(w3: Web3, token_address: str):
    return loadContract(w3, 'IUniswapV2ERC20.json', token_address)


def loadPair(w3: Web3, factory_address: str, token_a: str, token_b: str):
    factory = loadFactory(w3, factory_address)
    contract_a = loadToken(w3, token_a)
    contract_b = loadToken(w3, token_b)
    pair_address = factory.functions.getPair(contract_a.address, contract_b.address).call()
    contract_pair = loadContract(w3, 'IUniswapV2Pair.json', pair_address)
    return contract_pair


if __name__ == '__main__':
    w3_test = { 'w3': Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545')),
                'factory_address': '0x6725F303b657a9451d8BA641348b6761A6CC7a17',
                'token_a': '0xae13d989dac2f0debff460ac112a837c89baa7cd',
                'token_b': '0x15ee726884d4c409c0bc5ba3edf10981b2218843' }
    pair = loadPair(**w3_test)
    reserves = pair.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]
    print(f'The current price is : {reserve1/reserve0}')

    token_a = loadToken(w3_test['w3'], w3_test['token_a'])
    token_balance = token_a.functions.balanceOf(Web3.toChecksumAddress('0x8d06168710935bce9fe5720a729dc2660290f20a')).call()
    print(Web3.fromWei(token_balance, 'ether'))