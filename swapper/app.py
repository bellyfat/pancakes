import time
from web3 import Web3
 
PancakeABI = open('pancakeABI','r').read().replace('\n','')
 
wallet = {
    "address": "0xd46E81085952e2EF618DC9e185d9b363C3e3A883",
    "private": "d10aa6c590e6aa54a66ac3772453f2d739a20382e5d8bfcc46efa59a3a9d3945",
}

testnet = {
    'chainid': 97,
    'factory': '0x6725F303b657a9451d8BA641348b6761A6CC7a17',
    'router': '0xD99D1c33F9fC3444f8101754aBC46c52416550D1',
    'rpc': 'https://data-seed-prebsc-1-s1.binance.org:8545/',
    'spend': '0xae13d989dac2f0debff460ac112a837c89baa7cd', #testnet WBNB
    'contract': '0x15ee726884d4c409c0bc5ba3edf10981b2218843' #testnet fucktoken
}

chain = testnet

web3 = Web3(Web3.HTTPProvider(chain.get('rpc')))
if web3.isConnected() == False:
    print('cant connect')
    exit()

sender_address = wallet.get('address')
private = wallet.get('private')
balance = web3.eth.get_balance(sender_address)
balance -= 250000 * 21 * 5


router_address = chain.get('router')
spend = web3.toChecksumAddress(chain.get('spend'))
contract_id = web3.toChecksumAddress(chain.get('contract'))
 
# # #Setup the PancakeSwap contract
contract = web3.eth.contract(address=router_address, abi=PancakeABI)
nonce = web3.eth.get_transaction_count(sender_address)
 
start = time.time()
 
pancakeswap2_txn = contract.functions.swapExactETHForTokens(0, [spend, contract_id], sender_address, (int(time.time()) + 1000000)).buildTransaction({
    'from': sender_address,
    'value': web3.toWei(0.000001, 'Ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei(10, 'gwei'),
    'nonce': nonce,
    'chainId': chain.get('chainId')
    })
 
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private)
tx_token = web3.toHex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
print(f'https://testnet.bscscan.com/tx/{tx_token}')