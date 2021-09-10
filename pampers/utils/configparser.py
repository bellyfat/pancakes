import sys, os
from collections import OrderedDict, namedtuple

from dotenv import dotenv_values

def _verify_config(config: OrderedDict, variables: list):
    try:
        assert(all(k in variables for k in config.keys()))
    except Exception as e:
        print('config contains unkown values: %s', config.keys() - variables)
        pass
    try:
        assert(all(k in config.keys() for k in variables))
    except:
        raise Exception('invalid config')
    return config

def parse_chain(env_file: str):
    variables = ['ID', 'GAS_PRICE', 'EXPLORER', 'RPC', 'FACTORY', 'ROUTER', 'TOKEN_A', 'TOKEN_B']
    chainConfig = namedtuple('Chain', variables)
    config = _verify_config(dotenv_values(env_file), variables)
    chain = chainConfig(**config)
    return chain


def parse_env():
    variables = ['PRIVATE_KEY', 'NET', 'DEBUG']
    appConfig = namedtuple('App', variables)
    config = _verify_config(dotenv_values('.env'), variables)
    app = appConfig(**config)
    chain = parse_chain(f'.env.{app.NET}')
    root = namedtuple('Root', ['app', 'chain'])
    return root(app, chain)




if __name__ == '__main__':
    
    cfg = parse_env()
