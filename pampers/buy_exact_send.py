from pampers import APP, CHAIN
from pampers.contracts.helpers import loadPair


p = loadPair(CHAIN.get('FACTORY'), CHAIN.get('token_a'), CHAIN.get('token_b'))