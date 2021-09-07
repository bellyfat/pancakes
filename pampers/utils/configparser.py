import logging
import os

from collections import OrderedDict, namedtuple

from dotenv import dotenv_values
logger = logging.getLogger('configparser')
ch = logging.StreamHandler()
if os.getenv('DEBUG', 'True') == 'True':
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def _verify_config(config: OrderedDict, variables: list):
    try:
        assert(all(k in variables for k in config.keys()))
    except:
        logger.warning('config contains unkown values: %s', config.keys() - variables)
    try:
        assert(all(k in config.keys() for k in variables))
    except:
        logger.critical('config is missing mandatory values: %s', variables - config.keys())
    return config

def parse_chain(env_file: str):
    variables = ['ID', 'GAS_PRICE', 'EXPLORER', 'RPC', 'FACTORY', 'ROUTER', 'TOKEN_A', 'TOKEN_B']
    chainConfig = namedtuple('Chain', variables)
    config = _verify_config(dotenv_values(env_file), variables)
    chain = chainConfig(**config)
    logger.debug('parsed chain config for %s', env_file)
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
