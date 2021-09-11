import os
import json
from pathlib import Path
from pampers import w3, log

from web3.contract import Contract
abi_path = Path(os.path.dirname(os.path.realpath(__file__)))


def loadContract(abi_json: str, address: str) -> Contract:
    address = w3.toChecksumAddress(address)
    abi = json.load(open(abi_path.joinpath(abi_json), 'r'))['abi']
    contract_instance = w3.eth.contract(address=address, abi=abi)
    return contract_instance


def loadFactory(factory_address: str) -> Contract:
    return loadContract('IUniswapV2Factory.json', factory_address)


def loadRouter02(router_address: str) -> Contract:
    return loadContract('IUniswapV2Router02.json', router_address)


def loadToken(token_address: str) -> Contract:
    return loadContract('IUniswapV2ERC20.json', token_address)


def loadPair(factory: str, token_a: str, token_b: str) -> dict:
    factory = loadFactory(factory)
    contract_a = loadToken(token_a)
    contract_b = loadToken(token_b)
    pair_address = factory.functions.getPair(contract_a.address, contract_b.address).call()
    contract_pair = loadContract('IUniswapV2Pair.json', pair_address)
    return {'a': contract_a, 'b': contract_b, 'pair': contract_pair}
