from pampers.tx.builders import swap
from pampers.tx.senders import sign_and_send
from pampers.utils.accounts import account_nonce
import math
from eth_utils import Contract
from pampers import w3,CHAIN, acc, log, factory, contract_pair, router, token_a, token_b, contract_b, contract_a
# token a is always eth in this situation. contract a is wrapped eth used for uniswap functions 
# but the token balance of web3.eth api is taken instead
# so make sure your eth balance is not wrapped eth but regular eth
SLIPPERS = 0.90 # slippage in procent
tokens_per_swap = 200

def calculate_token_swap_value(tokens_per_swap: int,  token_to_swap: Contract, pair: Contract):
    t0, t1, timestamp =  pair.functions.getReserves().call()
    Kconstant = t0 * t1
    tokens = tokens_per_swap * 10 ** token_to_swap.functions.decimals().call()
    if pair.functions.token0().call() == token_to_swap.address:
        tokens += t0
        value = t1
    elif pair.functions.token1().call() == token_to_swap.address:
        tokens += t1
        value = t0
    else:
        raise Exception('trying to calculate wrong token swap value')
    return value - math.floor(Kconstant / tokens)





# nonce = account_nonce(acc)
# balance = w3.eth.get_balance(acc.address)
# swaptx = swap(nonce, acc.address, balance)
# value = swaptx['value'] #taxed balance so there is enough eth left for two more swaps 
# if value <= 0:
#     raise Exception('trying to swap with (near) empty wallets. Something went wrong')
# elif value < tokens_worth_balance:
#     log.debug('taxed balance on wallet is less than configured purchase amount. Defaulting to full balance swap')
#     tokens_per_swap = router.functions.getAmountOut(value, liquidity_a, liquidity_b).call()
# else:
#     swaptx = swap(nonce, acc.address, tokens_worth_balance)
# swap_txn = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
#     math.floor(tokens_per_swap * SLIPPERS),
#     [token_a, token_b],
#     acc.address,
#     (int(time.time()) + 1000000).buildTransaction(swaptx)
# )
# else:
#     swap_txn = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(tokens_per_swap,
#     [w3.toChecksumAddress(token_a), w3.toChecksumAddress(token_b)],
#     w3.toChecksumAddress(acc.address),
#     int(time.time()) + 1000000).buildTransaction(swaptx)
# hashed_tx = sign_and_send(swap_txn)
