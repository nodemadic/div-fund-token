# import brownie
# from brownie import chain


def test_round_closes(accounts, token):
    token.pledge(
        11000000000000000000, {"from": accounts[0], "amount": 11000000000000000000}
    )

    token.closeRound({"from": accounts[0]})

    assert token.balanceOf(accounts[0], {"from": accounts[1]}) > 25


# def xtest_mints_for_multiple_pledgers(accounts, token):
#     pass
