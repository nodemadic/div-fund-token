def test_can_create_simple_collectible(nft, accounts):
    nft.safeMint(accounts[0])

    assert nft.ownerOf(0) == accounts[0]
