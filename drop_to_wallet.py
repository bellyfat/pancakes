from pampers.utils.filewriters import csv_writer
from pampers.airdrop_wallets import airdrop
writer = csv_writer('airdrop', ['public_key', 'private_key', 'tx_hash'])
for row in airdrop(10):
    writer.writerow(row)