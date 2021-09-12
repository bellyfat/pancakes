from pampers import w3, log, contract_b, acc, contract_pair, contract_a, CHAIN
from web3 import Account
from pampers.tx.builders import swap
from pampers.tx.senders import sign_and_send
from pampers.utils.accounts import account_nonce
from pampers.contracts.helpers import loadRouter02
import math
import time
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
nonce = account_nonce(acc)
tokens = contract_b.functions.balanceOf(acc.address).call()
t0, t1, timestamp = contract_pair.functions.getReserves().call()
Kconstant = t0 * t1
if contract_pair.functions.token0().call() == contract_b.address:
    tokens += t0
    value = t1
elif contract_pair.functions.token1().call() == contract_b.address:
    tokens += t1
    value = t0
tokens_worth = math.floor(value - math.floor(Kconstant / tokens))

router = loadRouter02(CHAIN.get('ROUTER'))

swap_balance = contract_b.functions.balanceOf(acc.address).call()
tx = contract_b.functions.approve(CHAIN.get('ROUTER'), swap_balance).buildTransaction({
                                    'from': acc.address, 'nonce':  nonce})
signed_tx = w3.eth.account.sign_transaction(tx, acc.privateKey)
hashed_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(hashed_tx)
allowance = contract_b.functions.allowance(
    acc.address, CHAIN.get('ROUTER')).call()
print(allowance)
nonce = account_nonce(acc)
swaptx = {
    'nonce': nonce,
    'chainId': int(CHAIN.get('ID')),
    'gasPrice': w3.toWei(CHAIN.get('GAS_PRICE'), 'gwei'),
    'gas': 200000,
    'from': w3.toChecksumAddress(acc.address)
    }

swap_txn = router.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
    swap_balance,
    0,
    [contract_b.address, contract_a.address],
     w3.toChecksumAddress(acc.address),
    int(time.time()) + 1000000).buildTransaction(swaptx)

signed_txn=w3.eth.account.sign_transaction(swap_txn, acc.privateKey)
hashed_txn=w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt=w3.eth.wait_for_transaction_receipt(hashed_txn)
print(txn_receipt)