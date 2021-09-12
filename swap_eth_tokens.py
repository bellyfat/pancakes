from pampers import w3, log, acc, router, contract_a, contract_b, contract_pair
from web3 import Account
from pampers.tx.builders import swap
from pampers.tx.senders import sign_and_send
from pampers.utils.accounts import account_nonce
from web3.contract import Contract
import math
import time

def calculate_token_swap_value(tokens_per_swap: int,  contract_b: Contract, pair: Contract):
    t0, t1, timestamp = pair.functions.getReserves().call()
    Kconstant = t0 * t1
    tokens = tokens_per_swap * 10 ** contract_b.functions.decimals().call()
    if pair.functions.token0().call() == contract_b.address:
        tokens += t0
        value = t1
    elif pair.functions.token1().call() == contract_b.address:
        tokens += t1
        value = t0
    else:
        raise Exception('trying to calculate wrong token swap value')
    return value - math.floor(Kconstant / tokens)


def swap_value_to_tokens(account: Account, tokens_per_swap: int, router: Contract,
                         contract_a: Contract, contract_b: Contract, pair: Contract, SLIPPERS: float = 0.90):
    value = calculate_token_swap_value(tokens_per_swap, contract_b, contract_pair)
    nonce = account_nonce(account)
    balance = w3.eth.get_balance(account.address)
    tokens = tokens_per_swap * 10 ** contract_b.functions.decimals().call()
    token_a, token_b = contract_a.address, contract_b.address
    # taxed balance in key value so there is enough eth left for two more swaps
    swaptx = swap(nonce, account.address, balance)
    if swaptx['value'] <= 0:
        raise Exception(
            'trying to swap with (near) empty wallets. Something went wrong')
    elif swaptx['value'] > value:
        log.debug('wallet has more balance than configured txsize')
        swaptx = swap(nonce, account.address, value)

    swap_txn = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
        math.floor(SLIPPERS * tokens),
        [token_a, token_b],
        account.address,
        int(time.time()) + 1000000).buildTransaction(swaptx)
    return sign_and_send(swap_txn, account)


if __name__ == '__main__':
    print(swap_value_to_tokens(acc, 333333333333, router, contract_a, contract_b, contract_pair, 0.5))