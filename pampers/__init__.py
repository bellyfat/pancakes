import logging
import os
from web3 import Web3
from eth_account import Account

DEBUGFORMATTER = '%(filename)s:%(name)s:%(funcName)s:%(lineno)d: %(message)s'
"""Debug file formatter."""

INFOFORMATTER = '%(message)s'
"""Log file and stream output formatter."""


log = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
if os.getenv('DEBUG', 'True') == 'True':
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logging.Formatter(DEBUGFORMATTER))
    log.setLevel(logging.DEBUG)
else:
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(logging.Formatter(INFOFORMATTER))
    log.setLevel(logging.INFO)

log.addHandler(consoleHandler)

try:
    pkey = os.getenv('PRIVATE_KEY', '0000000000000000000000000000000000000000000000000000000000000001')
    if pkey == '0000000000000000000000000000000000000000000000000000000000000001':
        log.warning('using testing private key %s', pkey)
    acc = Account.from_key(pkey)
except Exception:
    log.critical('cant initialize account. Is your private key correct?')

rpc = os.getenv('RPC', 'https://data-seed-prebsc-1-s1.binance.org:8545')
w3 = Web3(Web3.HTTPProvider(rpc))
if w3.isConnected():
    log.debug('connected to rpc endpoint: %s', rpc)
else:
    log.critical('cant connect to rpc endpoint... exitting (%s)', rpc)
    raise Exception('rpc endpoint unavailable')