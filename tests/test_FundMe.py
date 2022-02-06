from brownie import accounts
import pytest
from scripts.helpful import get_account,LOCAL_BLOCKCHAIN_DEVELOPMENTS
from scripts.deploy import deploy_fundMe
from brownie import network,exceptions

def test_fund_and_withdraw():
    # get the account
    account=get_account()
    # get the contract
    fund_me=deploy_fundMe()
    # get the entrance fee
    entranceFEE=fund_me.getEntranceFee()
    # execute the transaction
    tx=fund_me.fund({"from":account,"value":entranceFEE})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entranceFEE
    tx2=fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0
def only_owner_withdraws():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENTS:
        print(network.show_active())
        pytest.skip(reason="only for local testing")
    account=get_account()
    fundme=deploy_fundMe()
    bad_actor=accounts.add()
    fundme.withdraw({"from":bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fundme.withdraw({"from":bad_actor})


