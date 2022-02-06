from time import sleep
from brownie import MockV3Aggregator,FundMe,accounts,network,config
from scripts.helpful import get_account,deploy_mocks,LOCAL_BLOCKCHAIN_DEVELOPMENTS
def deploy_fundMe():
    account=get_account()
    # pass pricefeed address to our fundme contract
    # if we are on a persistent network like rinkeby, use the associated address
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENTS:
        price_feed=config["networks"][network.show_active()]["eth_usd_price_feed"]
    # otherwise, deploy mocks
    else:
        deploy_mocks()
        price_feed=MockV3Aggregator[-1].address      
        

    fundme=FundMe.deploy(price_feed,{"from":account},publish_source=config["networks"][network.show_active()].get("verify"))
    print(f"Contract deployed to {fundme.address}")
    sleep(1)
    return fundme
    
    

def main():
    deploy_fundMe()