from brownie import Fundraise, accounts
from scripts.helpful_scripts import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")


def main():
    account = get_account()
    dividend_token = Fundraise.deploy(
        accounts[1],
        "Dividend",
        "DIV",
        1,
        5000000000000000000,
        {"from": account},
    )
    print(dividend_token.name())
    print(type(accounts[0]))
