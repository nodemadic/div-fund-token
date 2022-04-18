# import brownie
# from brownie import chain


def test_round_closes(accounts, token):
    token.pledge(
        11000000000000000000, {"from": accounts[0], "amount": 11000000000000000000}
    )

    token.closeRound({"from": accounts[0]})

    assert token.balanceOf(accounts[0], {"from": accounts[0]}) > 25


def test_mints_for_multiple_pledgers(accounts, token):
    token.pledge(
        6000000000000000000, {"from": accounts[0], "amount": 6000000000000000000}
    )
    token.pledge(
        3000000000000000000, {"from": accounts[1], "amount": 3000000000000000000}
    )
    token.pledge(
        2000000000000000000, {"from": accounts[2], "amount": 2000000000000000000}
    )

    token.closeRound({"from": accounts[0]})

    assert token.balanceOf(accounts[0], {"from": accounts[0]}) > 0
    assert token.balanceOf(accounts[1], {"from": accounts[1]}) > 0
    assert token.balanceOf(accounts[2], {"from": accounts[2]}) > 0


def test_mints_for_owner_without_owner_contribution(accounts, token):
    token.pledge(
        11000000000000000000, {"from": accounts[1], "amount": 11000000000000000000}
    )

    token.closeRound({"from": accounts[0]})

    assert token.balanceOf(accounts[0], {"from": accounts[0]}) > 0


def test_total_tokens_equals_intended_supply(accounts, token):
    token.pledge(
        6000000000000000000, {"from": accounts[0], "amount": 6000000000000000000}
    )
    token.pledge(
        3000000000000000000, {"from": accounts[1], "amount": 3000000000000000000}
    )
    token.pledge(
        2000000000000000000, {"from": accounts[2], "amount": 2000000000000000000}
    )

    token.closeRound({"from": accounts[0]})

    assert token.totalSupply() == 100000


def test_can_close_round_without_owner_contribution(accounts, token):
    token.pledge(
        6000000000000000000, {"from": accounts[1], "amount": 6000000000000000000}
    )
    token.pledge(
        3000000000000000000, {"from": accounts[2], "amount": 3000000000000000000}
    )
    token.pledge(
        2000000000000000000, {"from": accounts[3], "amount": 2000000000000000000}
    )

    token.closeRound({"from": accounts[0]})

    assert token.totalSupply() == 100000
