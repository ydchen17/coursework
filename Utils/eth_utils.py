from web3 import Web3, HTTPProvider
import shared
shared.init()
from Crypto.Hash import keccak

def connect_to_web3():
    """
    Connect to Web3 server.
    Args:
    Returns:
      res: Boolean indicating that connection was succeed or not.
      web3: Web3 Object
    """
    web3 = Web3(HTTPProvider('https://polygon-mainnet.infura.io/v3/2e12551e05084afc843d1b78ee95d420'))
    res = web3.isConnected()
    return res, web3


def get_decimal_token(contract):
    try:
        decimals = contract.functions.decimals().call()
    except:
        decimals = None
    return decimals

def obtain_hash_event(event):
    k = keccak.new(digest_bits=256)
    k.update(bytes(event, encoding='utf-8'))
    return '0x'+k.hexdigest()

def obtain_events_from_abi(abi: dict) -> list:
    events = []
    for function in abi:
        if function['type'] == 'event':
            event = function['name'] + '('
            for cont, element in enumerate(function['inputs']):
                if cont == 0:
                    event += element['type']
                else:
                    event += ','+element['type']
                cont += 1
            event  += ')'
            events.append(event)

    return events
