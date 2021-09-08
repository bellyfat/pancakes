import os
import json
import sys
from pathlib import Path

try:
    from pampers import w3
except Exception as e:
    sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__))).parents[1]))
    from pampers import w3

abi_path = Path(os.path.dirname(os.path.realpath(__file__)))


def loadContract(abi_json: str, address: str):
    address = w3.toChecksumAddress(address)
    abi = json.load(open(abi_path.joinpath(abi_json), 'r'))['abi']
    contract_instance = w3.eth.contract(address=address, abi=abi)
    return contract_instance


def loadFactory(factory_address: str):
    return loadContract('IUniswapV2Factory.json', factory_address)


def loadRouter(router_address: str):
    return loadContract('IUniswapV2Router.json', router_address)


def loadToken(token_address: str):
    return loadContract('IUniswapV2ERC20.json', token_address)


def loadPair(factory_address: str, token_a: str, token_b: str):
    factory = loadFactory(factory_address)
    contract_a = loadToken(token_a)
    contract_b = loadToken(token_b)
    pair_address = factory.functions.getPair(contract_a.address, contract_b.address).call()
    contract_pair = loadContract('IUniswapV2Pair.json', pair_address)
    return contract_pair


if __name__ == '__main__':
    _test = {'factory_address': '0x6725F303b657a9451d8BA641348b6761A6CC7a17',
             'token_a': '0xae13d989dac2f0debff460ac112a837c89baa7cd',
             'token_b': '0x15ee726884d4c409c0bc5ba3edf10981b2218843'}
    pair = loadPair(**_test)
    reserves = pair.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]
    print(f'The current price is : {reserve1/reserve0}')

    token_a = loadToken(_test['token_a'])
    token_balance = token_a.functions.balanceOf(toChecksumAddress('0x8d06168710935bce9fe5720a729dc2660290f20a')).call()
    print(w3.fromWei(token_balance, 'ether'))