import sys, os
from collections import OrderedDict, namedtuple
from pathlib import Path
try:
    from pampers import log
except Exception as e:
    sys.path.insert(0, str(Path(os.path.dirname(os.path.realpath(__file__))).parents[1]))
    from pampers import log

from dotenv import dotenv_values

def _verify_config(config: OrderedDict, variables: list):
    try:
        assert(all(k in variables for k in config.keys()))
    except:
        log.warning('config contains unkown values: %s', config.keys() - variables)
    try:
        assert(all(k in config.keys() for k in variables))
    except:
        log.critical('config is missing mandatory values: %s', variables - config.keys())
        raise Exception('invalid config')
    return config

def parse_chain(env_file: str):
    variables = ['ID', 'GAS_PRICE', 'EXPLORER', 'RPC', 'FACTORY', 'ROUTER', 'TOKEN_A', 'TOKEN_B']
    chainConfig = namedtuple('Chain', variables)
    config = _verify_config(dotenv_values(env_file), variables)
    chain = chainConfig(**config)
    log.info('parsed chain config for %s', env_file)
    return chain


def parse_env():
    variables = ['PRIVATE_KEY', 'NET', 'TUMBLE_DIR', 'SWAP_DIR']
    appConfig = namedtuple('App', variables)
    config = _verify_config(dotenv_values('.env'), variables)
    app = appConfig(**config)
    chain = parse_chain(f'.env.{app.NET}')
    root = namedtuple('Root', ['app', 'chain'])
    return root(app, chain)




if __name__ == '__main__':
    
    cfg = parse_env()
