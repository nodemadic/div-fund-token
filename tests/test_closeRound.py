# import brownie
# from brownie import chain


def test_round_closes(accounts, fundraise):
    fundraise.pledge(
        11000000000000000000, {"from": accounts[0], "amount": 11000000000000000000}
    )

    fundraise.closeRound({"from": accounts[0]})

    assert fundraise.balanceOf(accounts[0], {"from": accounts[0]}) > 25


def test_mints_for_multiple_pledgers(accounts, fundraise):
    fundraise.pledge(
        6000000000000000000, {"from": accounts[0], "amount": 6000000000000000000}
    )
    fundraise.pledge(
        3000000000000000000, {"from": accounts[1], "amount": 3000000000000000000}
    )
    fundraise.pledge(
        2000000000000000000, {"from": accounts[2], "amount": 2000000000000000000}
    )

    fundraise.closeRound({"from": accounts[0]})

    assert fundraise.balanceOf(accounts[0], {"from": accounts[0]}) > 0
    assert fundraise.balanceOf(accounts[1], {"from": accounts[1]}) > 0
    assert fundraise.balanceOf(accounts[2], {"from": accounts[2]}) > 0


def test_mints_for_owner_without_owner_contribution(accounts, fundraise):
    fundraise.pledge(
        11000000000000000000, {"from": accounts[1], "amount": 11000000000000000000}
    )

    fundraise.closeRound({"from": accounts[0]})

    assert fundraise.balanceOf(accounts[0], {"from": accounts[0]}) > 0


def test_total_tokens_equals_intended_supply(accounts, fundraise):
    fundraise.pledge(
        6000000000000000000, {"from": accounts[0], "amount": 6000000000000000000}
    )
    fundraise.pledge(
        3000000000000000000, {"from": accounts[1], "amount": 3000000000000000000}
    )
    fundraise.pledge(
        2000000000000000000, {"from": accounts[2], "amount": 2000000000000000000}
    )

    fundraise.closeRound({"from": accounts[0]})

    assert fundraise.totalSupply() == 100000


def test_can_close_round_without_owner_contribution(accounts, fundraise):
    fundraise.pledge(
        6000000000000000000, {"from": accounts[1], "amount": 6000000000000000000}
    )
    fundraise.pledge(
        3000000000000000000, {"from": accounts[2], "amount": 3000000000000000000}
    )
    fundraise.pledge(
        2000000000000000000, {"from": accounts[3], "amount": 2000000000000000000}
    )

    fundraise.closeRound({"from": accounts[0]})

    assert fundraise.totalSupply() == 100000
