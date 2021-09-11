from pampers import w3,CHAIN, acc, log
from pampers.tx.builders import swap
from pampers.tx.senders import sign_and_send
import time, math
from pampers.contracts.helpers import loadPair, loadRouter02, loadFactory
from pampers.utils.accounts import account_nonce
# token a is always eth in this situation. contract a is wrapped eth used for uniswap functions 
# but the token balance of web3.eth api is taken instead
# so make sure your eth balance is not wrapped eth but regular eth

factory = loadFactory(CHAIN.get('FACTORY'))
contracts = loadPair(w3.toChecksumAddress(factory.address), CHAIN.get('TOKEN_A'), CHAIN.get('TOKEN_B'))
DECIMALS = contracts.get('b').functions.decimals().call()
SLIPPERS = 0.90 # slippage in procent
max_tx_amount = 1000000000000000000 // 10 ** DECIMALS
## TODO: verify this really works 
tokens_per_swap = math.floor(max_tx_amount * 0.9)
exact_amount_tokens = tokens_per_swap #w3.toWei(tokens_per_swap, 'ether') # max receive 400 token B's per swap
router = loadRouter02(CHAIN.get('ROUTER'))
token0 = contracts.get('pair').functions.token0().call()
token1 = contracts.get('pair').functions.token1().call()
## token a is always eth or bnb in this script
if w3.toChecksumAddress(contracts.get('a').address) == token0:
    token_a = token0
    token_b = token1
    liquidity_a, liquidity_b, timestamp = contracts.get('pair').functions.getReserves().call()
elif w3.toChecksumAddress(contracts.get('a').address) == token1:
    log.warning('token a (eth) is token1 in sort order')
    token_a = token1
    token_b = token0
    liquidity_b, liquidity_a, timestamp = contracts.get('pair').functions.getReserves().call()
nonce = account_nonce(acc)
balance = w3.eth.get_balance(acc.address)
swaptx = swap(nonce, acc.address, balance)
value = swaptx['value']
tokens_is_worth_balance = router.functions.getAmountIn(exact_amount_tokens, liquidity_a, liquidity_b).call()
if value < tokens_is_worth_balance:
    print(tokens_is_worth_balance)
    print(value)
    exact_amount_tokens = router.functions.getAmountOut(value, liquidity_a, liquidity_b).call()

swap_txn = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(exact_amount_tokens,
    [w3.toChecksumAddress(token_a), w3.toChecksumAddress(token_b)],
    w3.toChecksumAddress(acc.address),
    int(time.time()) + 1000000).buildTransaction(swaptx)
hashed_tx = sign_and_send(swap_txn)
