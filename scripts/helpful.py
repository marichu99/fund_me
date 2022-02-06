from brownie import network,accounts,config,MockV3Aggregator
from web3 import Web3
FORKED_LOCAL_ENVIRONMENTS=["mainnet-fork","mainnet-fork-dev"]
DECIMALS=18
STARTING_PRICE=2000
LOCAL_BLOCKCHAIN_DEVELOPMENTS=["development","ganache-local"]
def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_DEVELOPMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        account = accounts.add(config["wallet"]["from-key"])
        return account
def deploy_mocks():
    print(f"The network we've deployed on is{network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator)<=0:
        MockV3Aggregator.deploy(DECIMALS,Web3.toWei(STARTING_PRICE,"ether"),{"from":get_account()})
        print("Mocks deployed!")