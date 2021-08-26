import time
from web3 import Web3
from eth_account import Account
from utils import json_privates_loader
from chains import bsc_testnet as chain

PancakeABI = open('pancakeABI','r').read().replace('\n','')


web3 = Web3(Web3.HTTPProvider(chain.get('rpc')))
gasPrice =  chain.get('gasPrice')
chain_id = chain.get('chainId')
if web3.isConnected() == False:
    print('cant connect')
    exit()


privates = json_privates_loader()
router_address = chain.get('router')
spend = web3.toChecksumAddress(chain.get('spend'))
contract_id = web3.toChecksumAddress(chain.get('contract'))
contract = web3.eth.contract(address=router_address, abi=PancakeABI)

swapgas = 250000
for p in privates:
    acc = Account.privateKeyToAccount(p)
    balance = web3.eth.get_balance(acc.address)
    nonce = web3.eth.get_transaction_count(acc.address)
    while True:
        value = balance - web3.toWei(gasPrice, 'gwei') * swapgas
        if value < 0:
            print(f'not enough balance for {acc.address}')
            break
        pancakeswap2_txn = contract.functions.swapExactETHForTokens(0, [spend, contract_id], acc.address, (int(time.time()) + 1000000)).buildTransaction({
            'from': acc.address,
            'value': value,
            'gas': swapgas,
            'gasPrice': web3.toWei(gasPrice, 'gwei'),
            'nonce': nonce,
            'chainId': chain_id
            })
        signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=p)
        try:
            tx_token = web3.toHex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
            print(f'https://testnet.bscscan.com/tx/{tx_token}')
            break
        except Exception as e:
            err = e.args[0]
            if err['message'] == 'transaction underpriced':
                gasPrice += 1
            else:
                print('fatal error occurred')
                print(e)
                exit()
