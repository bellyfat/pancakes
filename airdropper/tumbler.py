from utils import dict_to_file
import time
import random
from utils import json_private_loader, create_wallet
from chains import bsc_testnet as chain
from web3 import Web3
from eth_account import Account

TUMBLE_AMOUNT = 15 #amount of tumbles to obscure origin


web3 = Web3(Web3.HTTPProvider(chain.get('rpc')))

if web3.isConnected() == False:
    print('cant connect')
    exit()

def transfer_value(w3: Web3, chain: dict, addr_a: Account, addr_b: Account):
    swapgas = 21000
    gasPrice =  chain.get('gasPrice')
    chain_id = chain.get('chainId')
    balance = web3.eth.get_balance(addr_a.address)
    mempool = web3.geth.txpool.content()
    while True:
        if addr_a.address not in mempool['queued'] and addr_a.address not in mempool['pending']:
            break
        time.sleep(0.5)
        mempool = web3.geth.txpool.content()
    success = False
    while True:
        value = balance - web3.toWei(gasPrice, 'gwei') * swapgas
        if value < 0:
            return False
        nonce = web3.eth.get_transaction_count(addr_a.address)
        tx = { 
            'nonce': nonce,
            'chainId': chain_id,
            'to': addr_b.address,
            'value': value, 
            'gas': swapgas, 
            'gasPrice': web3.toWei(gasPrice, 'gwei')
        }
        signed_txn = web3.eth.account.sign_transaction(tx, addr_a.privateKey)
        try:
            tx_token = web3.toHex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
            print(f"{chain.get('explorer')}{tx_token}")
            success = True
            break
        except Exception as e:
            err = e.args[0]
            if err['message'] == 'transaction underpriced':
                gasPrice += 1
            else:
                print('fatal error occurred')
                print(e)
                success = False
                break
    return success
    


if __name__ == '__main__':

    for i in range(1, TUMBLE_AMOUNT):
        privates = json_private_loader()
        print(f'starting tumble {i} of {TUMBLE_AMOUNT} with {len(privates)} wallets --------')
        empty, full = [], []
        for private in privates:
            acc = Account.privateKeyToAccount(private)
            balance = web3.eth.get_balance(acc.address)
            if balance > 0:
                full.append(acc)
            elif balance == 0:
                empty.append(acc)

        if len(full) == 0:
            raise Exception('no full wallets found for tumbling')
        else:
            print(f'tumbling {len(full)} full wallets')     
        for acc in full:
            randomizer = random.randint(2, 4)
            if randomizer % 2 == 1 or len(empty) == 0:
                addr_b = create_wallet()
                d = {'private': addr_b.privateKey.hex(), 'address': addr_b.address}
                prefix = f'tumble_{i}'
                if i + 1 == TUMBLE_AMOUNT:
                    prefix = f'swapr_{i}'
                if transfer_value(web3, chain, acc, addr_b):
                    dict_to_file(d, prefix)
            else:
                addr_b = empty.pop(random.randint(1, len(empty)) - 1)            
                if transfer_value(web3, chain, acc, addr_b):
                    if i + 1 == TUMBLE_AMOUNT:
                        d = {'private': addr_b.privateKey.hex(), 'address': addr_b.address}
                        dict_to_file(d, f'swapr_{i}')
                else:
                    print('fatal error')
                    exit(0)