'''splits up full balance of a wallet to 10 new wallets'''
from pampers.utils.filewriters import csv_writer
from pampers.airdrop_wallets import airdrop
amount_wallets = 10
writer = csv_writer('airdrop', ['public_key', 'private_key', 'tx_hash'])
for row in airdrop(amount_wallets):
    writer.writerow(row)