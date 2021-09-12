from pampers.airdrop_balance import airdrop
from pampers.utils.filewriters import csv_writer

balance = 0.01
writer = csv_writer('airdrop', ['public_key', 'private_key', 'balance', 'tx_hash'])

for row in airdrop(balance):
    writer.writerow(row)