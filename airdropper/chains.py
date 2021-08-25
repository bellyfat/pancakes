bsc_testnet = { 
    'chainid' : 97, 
    'explorer' : 'testnet.bscscan.com/tx/',
    'http' : [ 
        'https://data-seed-prebsc-1-s1.binance.org:8545/', 
        'https://data-seed-prebsc-1-s2.binance.org:8545/', 
        'https://data-seed-prebsc-1-s3.binance.org:8545/'
    ],
    'wss' : [ 
        'wss://bsc.getblock.io/testnet/?api_key=0f16f3f7-b29a-45d8-9c68-83c4b0de9e1b'
    ],
    'gas': 200000,
    'gasPrice': 10 # in gwei
}

bsc = {
    'chainid': 56,
    'explorer': 'bscscan.com/tx/',
    'http': [
        'https://bsc-dataseed.binance.org/',
        'https://bsc-dataseed1.defibit.io/',
        'https://bsc-dataseed1.ninicoin.io/'
    ],
    'wss': [
        'wss://bsc-ws-node.nariox.org:443'
    ],
    'gas': 200000,
    'gasPrice': 10 # in gwei
}

#The rate limit of BSC endpoint on Testnet and Mainnet is 10K/5min.