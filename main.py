from pampers.utils.configparser import parse_env
from bot.airdrop import calculate_over_amount_wallets
from web3 import Web3

cfg = parse_env()

w3 = Web3(Web3.HTTPProvider(os.getenv('RPC','https://data-seed-prebsc-1-s1.binance.org:8545')))
amount_wallets = 5
balance, per_wallet = calculate_over_amount_wallets(w3, 5)
print(per_wallet)

