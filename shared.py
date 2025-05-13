import configparser
import subprocess
import pandas as pd
from web3 import Web3
from web3_multicall import Multicall
import json


def init():
    global INFURA_URL
    global USE_POOL_INFURA
    global USE_WALLET_INFURA
    global API_KEY

    global QUICKSWAP_FACTORY
    global SUSHISWAP_FACTORY
    global JETSWAP_FACTORY
    global POLYCAT_FACTORY
    global APESWAP_FACTORY
    global WAULTSWAP_FACTORY
    global DELFY_FACTORY

    global QUICKSWAP_ADDRESS
    global SUSHISWAP_ADDRESS
    global JETWSWAP_ADDRESS
    global POLYCAT_ADDRESS
    global APESWAP_ADDRESS
    global WAULTSWAP_ADDRESS
    global DELFY_ADDRESS
    global PRIVATE_KEY

    global EXCHANGES
    global DEX_CREATION
    global FACTORIES
    global FEE
    global ETH_ADDRESS
    global DEAD_ADDRESS
    global WMATIC
    global TOKEN_TOLERANCE
    global POOLS
    global FAKE_POOL
    global MULTICALL_CONTRACT
    global TRANSACTION
    global SYNC
    global CREATE

    global ROOT_FOLDER
    global WEEK
    global ABI
    global ABI_FACTORY
    global BLOCKSTUDY
    global ABI_POOL
    global ABI_ROUTER
    global IMPORTANT_TOKENS
    global web3
    global multicall
    global NO_ARB_ID
    global UNISWAP_V3_FACTORY
    global UNISWAP_V2_FACTORY
    global SUSHI_ABI_FACTORY
    global LOCAL_NONCE
    global timestamp_study

    ROOT_FOLDER = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, universal_newlines=True,
                                 stdout=subprocess.PIPE).stdout.strip()
    config = configparser.ConfigParser()
    config.read(ROOT_FOLDER + "/config.ini")

    # # Get infura node url and logic booleans
    INFURA_URL = config.get("NODE", "INFURA_URL")
    USE_POOL_INFURA = config.getboolean("NODE", "USE_POOL_INFURA")
    USE_WALLET_INFURA = config.getboolean("NODE", "USE_WALLET_INFURA")

    # Get etherscan keys
    API_KEY = config.get("APIS", "ETHERSCAN_API_KEY")

    # Get tokens addresses
    ETH_ADDRESS = config.get("ADDRESS", "ETH_ADDRESS")
    DEAD_ADDRESS = config.get("ADDRESS", "DEAD_ADDRESS")
    WETH = config.get("ADDRESS", "WETH_ADDRESS")
    WMATIC = config.get("ADDRESS", "WMATIC_ADDRESS")
    MULTICALL_CONTRACT = config.get("ADDRESS", "MULTICALL_CONTRACT")

    # Get routers addresses
    QUICKSWAP_ADDRESS = config.get("ROUTERS", "QUICKSWAP_ADDRESS")
    SUSHISWAP_ADDRESS = config.get("ROUTERS", "SUSHISWAP_ADDRESS")
    JETWSWAP_ADDRESS = config.get("ROUTERS", "JETWSWAP_ADDRESS")
    POLYCAT_ADDRESS = config.get("ROUTERS", "POLYCAT_ADDRESS")
    APESWAP_ADDRESS = config.get("ROUTERS", "APESWAP_ADDRESS")
    WAULTSWAP_ADDRESS = config.get("ROUTERS", "WAULTSWAP_ADDRESS")
    DELFY_ADDRESS = config.get("ROUTERS", "DELFY_ADDRESS")

    FAKE_POOL = config.get("POOLS", "FAKE_POOL")

    # Get pools factories
    UNISWAP_V3_FACTORY = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
    UNISWAP_V2_FACTORY = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
    QUICKSWAP_FACTORY = config.get("FACTORIES", "QUICKSWAP_FACTORY")
    SUSHISWAP_FACTORY = config.get("FACTORIES", "SUSHISWAP_FACTORY")
    JETSWAP_FACTORY = config.get("FACTORIES", "JETSWAP_FACTORY")
    POLYCAT_FACTORY = config.get("FACTORIES", "POLYCAT_FACTORY")
    APESWAP_FACTORY = config.get("FACTORIES", "APESWAP_FACTORY")
    WAULTSWAP_FACTORY = config.get("FACTORIES", "WAULTSWAP_FACTORY")
    DELFY_FACTORY = config.get("FACTORIES", "DELFY_FACTORY")
    # Get log hashes
    SYNC = config.get("LOG_HASHES", "SYNC")
    TRANSACTION = config.get("LOG_HASHES", "TRANSACTION")
    CREATE = config.get("LOG_HASHES", "CREATE")
    # Exchanges

    EXCHANGES = {
        "quickswap": QUICKSWAP_ADDRESS,
        "sushiswap": SUSHISWAP_ADDRESS,
        "jetwswap": JETWSWAP_ADDRESS,
        "polycat": POLYCAT_ADDRESS,
        "apeswap": APESWAP_ADDRESS,
        "waultswap": WAULTSWAP_ADDRESS,
        "delfy": DELFY_ADDRESS

    }
    DEX_CREATION = {
        "quickswap": 4931780,
        "sushiswap": 11333218,
        "jetwswap": 16569374,
        "polycat": 17703715,
        "apeswap": 15298801,
        "waultswap": 15474856,
        "defly": 5436831
    }
    FACTORIES = {
        "quickswap": QUICKSWAP_FACTORY,
        "sushiswap": SUSHISWAP_FACTORY,
        "jetwswap": JETSWAP_FACTORY,
        "polycat": POLYCAT_FACTORY,
        "apeswap": APESWAP_FACTORY,
        "waultswap": WAULTSWAP_FACTORY,
        "defly": DELFY_FACTORY
    }
    FEE = 0.003

    TOKEN_TOLERANCE = float(config.get("THRESHOLDS", "TOKEN_TOLERANCE"))
    # Define other globals not saved in config.ini
    WEEK = 4 * 60 * 24 * 7
    ABI = open(ROOT_FOLDER + "/normal_token_abi.txt").read()
    ABI_FACTORY = open(ROOT_FOLDER + "/factory_abi.txt").read()
    SUSHI_ABI_FACTORY = """[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]"""
    ABI_POOL = open(ROOT_FOLDER + "/abi_pool.txt").read()
    ABI_ROUTER = open(ROOT_FOLDER + "/abi_router.txt").read()
    # Define global objects
    BLOCKSTUDY = 27476347
    timestamp_study = 1650710999

    #
    PRIVATE_KEY = ""

    # POOLS = pd.read_csv(ROOT_FOLDER + "/Analysis/pools.csv")
    IMPORTANT_TOKENS = [WMATIC, "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
                        "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"]
    NO_ARB_ID = "518f45670b4e5be74905294047a80151"

    web3 = Web3(Web3.HTTPProvider(INFURA_URL))
    multicall = Multicall(web3.eth, address='0x11ce4B23bD875D7F5C6a31084f55fDe1e9A87507')
