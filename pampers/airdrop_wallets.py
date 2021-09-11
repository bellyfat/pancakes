from pampers import w3, acc, log, CHAIN

from pampers.tx.builders import transfer
from pampers.tx.senders import sign_and_send
from pampers.utils.accounts import account_new, account_nonce


def calculate_balance_per_wallet(amount: int = 30):
    '''spreads the available balance over a fixed mount of wallets'''
    balance = w3.eth.get_balance(acc.address)
    if balance == 0:
        raise Exception('airdropping wallet has no balance')
    balance_per_wallet = balance // amount
    log.debug('calculated %s ether to %s wallets',
              w3.fromWei(balance_per_wallet, 'ether'), amount)
    return balance_per_wallet

def airdrop(n: int = 3):
    balance_per_wallet = calculate_balance_per_wallet(n)
    num = account_nonce(acc)
    n += num
    while num < n:
        receiver = account_new()
        rawtx = transfer(nonce=num,
                         to_address = receiver.address, 
                         value = balance_per_wallet)
        row = { 'public_key': receiver.address,
                'private_key': receiver.privateKey.hex(),
                'tx_hash': str(None) }
        try:
            tx_hash = sign_and_send(rawtx, check_mempool=False)
            row['tx_hash'] = f"{CHAIN.get('EXPLORER')}/tx/{tx_hash}"
        except Exception as e:
            log.critical('something went wrong during transacting. Last known receiver private key: %s and public key: %s', receiver.address, receiver.privateKey.hex())
            print(e)
            raise
        finally:
            yield row
            num += 1