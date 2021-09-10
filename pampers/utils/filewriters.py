import os
import sys
import csv
from pathlib import Path
try:
    from pampers import log
except Exception as e:
    sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__))).parents[1]))
    from pampers import log
from pampers import CHAIN, APP

def csv_writer(fname: str = 'airdrop', header: list = ['public_key', 'private_key', 'tx_hash']) -> csv.DictWriter:
    stamp = CHAIN.get('TIMESTAMP')
    fname = f"{APP.get('NET')}-{stamp}_{fname}"
    if not fname.endswith('.csv'):
        fname = f'{fname}.csv'
    if os.path.isfile(fname):
        log.critical('please look at %s and rename it', fname)
        raise Exception('airdrop outfile already exists. Retrying too soon?')
    log.debug('creating csv file %s with headers %s', fname, header)
    csvfile = open(fname, "w", newline='')
    writer = csv.DictWriter(csvfile, fieldnames=header, dialect='excel')
    writer.writeheader()
    return writer
