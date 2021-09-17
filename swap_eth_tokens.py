from pampers import w3, log, router, contract_a, contract_b, contract_pair, acc
from web3 import Account
from pampers.tx.builders import swap
from pampers.tx.senders import sign_and_send
from pampers.utils.accounts import account_nonce
import math
import time
'''swaps a specific amount of tokens worth of eth to tokens'''
def calculate_token_swap_value(tokens_per_swap: int):
    t0, t1, timestamp = contract_pair.functions.getReserves().call()
    Kconstant = t0 * t1
    tokens = tokens_per_swap * 10 ** contract_b.functions.decimals().call()
    if contract_pair.functions.token0().call() == contract_b.address:
        tokens += t0
        value = t1
    elif contract_pair.functions.token1().call() == contract_b.address:
        tokens += t1
        value = t0
    else:
        raise Exception('trying to calculate wrong token swap value')
    ###returns value in eth 
    return value - math.floor(Kconstant / tokens)


def swap_value_to_tokens(account: Account, tokens_per_swap: int, SLIPPERS: float = 0.90):
    value = calculate_token_swap_value(tokens_per_swap)
    nonce = account_nonce(account)
    balance = w3.eth.get_balance(account.address)
    tokens = tokens_per_swap * 10 ** contract_b.functions.decimals().call()
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
        [contract_a.address, contract_b.address],
        account.address,
        int(time.time()) + 1000000).buildTransaction(swaptx)
    return sign_and_send(swap_txn, account)

def swap_balance_to_tokens(account: Account, value: float = 0.1):
    # value is noted in bnb
    value = w3.toWei(value, 'ether')
    nonce = account_nonce(account)
    balance = w3.eth.get_balance(account.address)
    if balance < value:
        log.warning('configured swap size which is higher than wallet balance. swapping whole balance')
        # taxed balance in key value so there is enough eth left for two more swaps
        swaptx = swap(nonce, account.address, balance)
    else:
        swaptx = swap(nonce, account.address, value)

    swap_txn = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
        0,
        [contract_a.address, contract_b.address],
        account.address,
        int(time.time()) + 1000000).buildTransaction(swaptx)
    return sign_and_send(swap_txn, account)


if __name__ == '__main__':
    acc = Account.from_key(acc.privateKey.hex())
    print(swap_value_to_tokens(acc, 333333333333, 0.9))
    print(swap_balance_to_tokens(acc, 0.01))