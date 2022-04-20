# from ctypes import addressof
import brownie


def test_can_create_listing(listings, nft, accounts):
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

    assert listings.listings(0, {"from": accounts[1]}) != 0


def test_cannot_create_listing_without_approval(listings, nft, accounts):
    nft.safeMint(accounts[0], {"from": accounts[0]})
    nft_token_id = 0
    nft_address = nft

    with brownie.reverts():
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


def test_contract_receives_nft(listings, nft, accounts):

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

    assert nft.ownerOf(0) == listings
