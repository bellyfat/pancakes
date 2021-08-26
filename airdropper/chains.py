bsc_testnet = { 
    'chainid' : 97, 
    'explorer' : 'testnet.bscscan.com/tx/',
    'factory': '0x6725F303b657a9451d8BA641348b6761A6CC7a17',
    'router': '0xD99D1c33F9fC3444f8101754aBC46c52416550D1',
    'rpc': 'https://data-seed-prebsc-1-s1.binance.org:8545/',
    'spend': '0xae13d989dac2f0debff460ac112a837c89baa7cd', #testnet WBNB
    'contract': '0x15ee726884d4c409c0bc5ba3edf10981b2218843', #testnet fucktoken
    'http' : [ 
        'https://data-seed-prebsc-1-s1.binance.org:8545/', 
        'https://data-seed-prebsc-1-s2.binance.org:8545/', 
        'https://data-seed-prebsc-1-s3.binance.org:8545/'
    ],
    'wss' : [ 
        'wss://bsc.getblock.io/testnet/?api_key=0f16f3f7-b29a-45d8-9c68-83c4b0de9e1b'
    ],
    'gasPrice': 5 # in gwei
}

bsc = {
    'chainid': 56,
    'explorer': 'bscscan.com/tx/',
    'factory': '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73',
    'router': '0x10ED43C718714eb63d5aA57B78B54704E256024E',
    'rpc': 'https://bsc-dataseed.binance.org/',
    'spend': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', #bsc mainnet WBNB
    'contract': '0xc748673057861a797275CD8A068AbB95A902e8de', #bsc mainnet baby Doge
    'http': [
        'https://bsc-dataseed.binance.org/',
        'https://bsc-dataseed1.defibit.io/',
        'https://bsc-dataseed1.ninicoin.io/'
    ],
    'wss': [
        'wss://bsc-ws-node.nariox.org:443'
    ],
    'gas': 200000,
    'gasPrice': 1 # in gwei
}

#The rate limit of BSC endpoint on Testnet and Mainnet is 10K/5min.