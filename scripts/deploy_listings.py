from brownie import Listings, MyToken
from scripts.helpful_scripts import get_account


def deploy_listings_contract():
    account = get_account()
    listings = Listings.deploy({"from": account})
    return listings


def deploy_nft_contract():
    account = get_account()
    nft = MyToken.deploy({"from": account})
    return nft


def main():
    deploy_listings_contract()
    deploy_nft_contract()
