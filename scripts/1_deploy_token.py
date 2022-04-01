from brownie import DividendTokenERC20
from scripts.helpful_scripts import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")


def main():
    account = get_account()
    dividend_token = DividendTokenERC20.deploy(100000, {"from": account})
    print(dividend_token.name())
