import math

from pampers import w3, acc, log, CHAIN
from pampers.tx.builders import transfer
from pampers.tx.senders import sign_and_send
from pampers.utils.accounts import account_new, account_nonce


def airdrop(amount: float = 0.01):
    '''amount is measured in ether/bnb so 0.01 bnb or 0.1 bnb. returns amount of wallets to airdrop. Doesn't include gas fees'''
    balance = w3.eth.get_balance(acc.address)
    if balance == 0:
        raise Exception('airdropping wallet has no balance')
    n = math.floor(balance / w3.toWei(amount, 'ether'))
    num = account_nonce(acc)
    n += num
    while num < n:
        receiver = account_new()
        rawtx = transfer(nonce=num,
                         to_address = receiver.address, 
                         value = w3.toWei(amount,'ether'))
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
