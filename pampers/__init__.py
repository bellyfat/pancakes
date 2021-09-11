import logging

import time
from web3 import Web3
from eth_account import Account
from pampers.utils.configparser import parse_env
CONFIG = parse_env()
APP = CONFIG.app._asdict()
CHAIN = {
    'TIMESTAMP': str(int(time.time())),
    **CONFIG.chain._asdict()
}


DEBUGFORMATTER = '%(filename)s:%(name)s:%(funcName)s:%(lineno)d: %(message)s'
"""Debug file formatter."""

INFOFORMATTER = '%(message)s'
"""Log file and stream output formatter."""


log = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
if APP.get('DEBUG') == 'True':
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logging.Formatter(DEBUGFORMATTER))
    log.setLevel(logging.DEBUG)
else:
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(logging.Formatter(INFOFORMATTER))
    log.setLevel(logging.INFO)

log.addHandler(consoleHandler)


try:
    acc = Account.from_key(APP.get('PRIVATE_KEY'))
except Exception:
    log.critical('cant initialize account. Is your private key correct?')
    raise

rpc = CHAIN.get('RPC')

w3 = Web3(Web3.HTTPProvider(rpc))
if w3.isConnected():
    log.debug('connected to rpc endpoint: %s', rpc)
else:
    log.critical('cant connect to rpc endpoint... exitting (%s)', rpc)
    raise Exception('rpc endpoint unavailable')
from pampers.contracts.helpers import loadPair, loadRouter02, loadFactory, loadToken
token_a =  w3.toChecksumAddress(CHAIN.get('TOKEN_A'))
token_b =  w3.toChecksumAddress(CHAIN.get('TOKEN_B'))
router = loadRouter02(CHAIN.get('ROUTER'))
factory = loadFactory(CHAIN.get('FACTORY'))
contract_pair = loadPair(w3.toChecksumAddress(factory.address), token_a, token_b)
contract_a = loadToken(CHAIN.get('TOKEN_A'))
contract_b = loadToken(CHAIN.get('TOKEN_B'))
