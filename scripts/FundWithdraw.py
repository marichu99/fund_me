from brownie import FundMe, accounts
from scripts.helpful import get_account
def fund():
    fund=FundMe[-1]
    account=get_account()
    entranceFEE=fund.getEntranceFee()
    print(f"The current entry fee is {entranceFEE}")
    fund.fund({"from":account,"value":entranceFEE})
def withdraw():
    fund_me=FundMe[-1]
    account=get_account()
    fund_me.withdraw({"from":account})
def main():
    fund()
    withdraw()