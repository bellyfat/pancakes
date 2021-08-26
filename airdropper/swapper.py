import time
from web3 import Web3
from eth_account import Account
from utils import json_privates_loader
PancakeABI = open('pancakeABI','r').read().replace('\n','')
 
testnet = {
    'chainid': 97,
    'gasPrice': 10,
    'factory': '0x6725F303b657a9451d8BA641348b6761A6CC7a17',
    'router': '0xD99D1c33F9fC3444f8101754aBC46c52416550D1',
    'rpc': 'https://data-seed-prebsc-1-s1.binance.org:8545/',
    'spend': '0xae13d989dac2f0debff460ac112a837c89baa7cd', #testnet WBNB
    'contract': '0x15ee726884d4c409c0bc5ba3edf10981b2218843' #testnet fucktoken
}

chain = testnet

web3 = Web3(Web3.HTTPProvider(chain.get('rpc')))
gasPrice =  web3.toWei(chain.get('gasPrice'), 'gwei')
if web3.isConnected() == False:
    print('cant connect')
    exit()


privates = json_privates_loader()
router_address = chain.get('router')
spend = web3.toChecksumAddress(chain.get('spend'))
contract_id = web3.toChecksumAddress(chain.get('contract'))
contract = web3.eth.contract(address=router_address, abi=PancakeABI)

for p in privates:
    acc = Account.privateKeyToAccount(p)
    balance = web3.eth.get_balance(acc.address)
    balance -= gasPrice * 200000
    print(balance)
    nonce = web3.eth.get_transaction_count(acc.address)
 
    start = time.time()
    pancakeswap2_txn = contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(0, [spend, contract_id], acc.address, (int(time.time()) + 1000000)).buildTransaction({
        'from': acc.address,
        'value': balance,
        'gas': 200000,
        'gasPrice':gasPrice,
        'nonce': nonce,
        'chainId': chain.get('chainId')
        })
    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=p)
    tx_token = web3.toHex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
    print(f'https://testnet.bscscan.com/tx/{tx_token}')
# pancakeswap2_txn = contract.functions.swapExactETHForTokens(0, [spend, contract_id], sender_address, (int(time.time()) + 1000000)).buildTransaction({
#     'from': sender_address,
#     'value': web3.toWei(0.000001, 'Ether'),
#     'gas': 2000000,
#     'gasPrice': web3.toWei(10, 'gwei'),
#     'nonce': nonce,
#     'chainId': chain.get('chainId')
#     })



 

