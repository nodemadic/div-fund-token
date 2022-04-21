import brownie
from brownie import chain, Fundraise
from brownie.network.contract import Contract


def create_listing(listings, nft, accounts):
    nft.safeMint(accounts[0], {"from": accounts[0]})
    nft.approve(listings, 0, {"from": accounts[0]})
    nft_token_id = 0
    nft_address = nft

    listings.createListing(
        nft_address,
        nft_token_id,
        accounts[0],
        "Test1",
        "T1",
        1,
        10000000000000000000,
        {"from": accounts[0]},
    )


def wait_past_deadline():
    chain.sleep(40000)
    chain.mine()


def create_fundraise_instance(listings, listing_id):
    fundraise_abi = Fundraise.abi
    fundraise_contract = Contract.from_abi(
        "Fundraise",
        listings.getListingFundraiseContract(listing_id),
        fundraise_abi,
    )
    return fundraise_contract


def create_successful_raise(listings, accounts):
    fundraiseContract = create_fundraise_instance(listings, 0)
    fundraiseContract.pledge(
        10000000000000000000, {"from": accounts[1], "amount": 10000000000000000000}
    )


def test_can_withdraw_after_unsuccessful_raise(listings, nft, accounts):
    create_listing(listings, nft, accounts)
    wait_past_deadline()

    listings.unsuccessfulRaiseWithdrawNFT(0, {"from": accounts[0]})

    assert nft.ownerOf(0) == accounts[0]


def test_cannot_withdraw_after_successful_raise(listings, nft, accounts):
    create_listing(listings, nft, accounts)

    create_successful_raise(listings, accounts)
    wait_past_deadline()

    with brownie.reverts():
        listings.unsuccessfulRaiseWithdrawNFT(0, {"from": accounts[0]})


def test_cannot_withdraw_before_deadline(listings, nft, accounts):
    create_listing(listings, nft, accounts)

    with brownie.reverts():
        listings.unsuccessfulRaiseWithdrawNFT(0, {"from": accounts[0]})
