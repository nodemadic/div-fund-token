import brownie
from brownie import chain


def test_can_pledge_before_deadline(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    fundraise.pledge(amount, {"from": accounts[0], "amount": amount})

    assert accounts[0].balance() <= pledger_original_balance - amount


def test_cannot_pledge_after_deadline(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    chain.sleep(4000)
    chain.mine()

    with brownie.reverts():
        fundraise.pledge(amount, {"from": accounts[0], "amount": amount})


# Must wait for future functions to be tested
def test_cannot_pledge_if_token_already_minted(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 10

    fundraise.pledge(amount, {"from": accounts[1], "amount": amount})
    fundraise.closeRound({"from": accounts[0]})

    with brownie.reverts():
        fundraise.pledge((amount // 1), {"from": accounts[0], "amount": amount})


def test_cannot_pledge_if_already_raised_enough(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 10
    maxAmount = (amount * 5) / 4

    fundraise.pledge(maxAmount, {"from": accounts[1], "amount": (maxAmount)})

    with brownie.reverts():
        fundraise.pledge(1, {"from": accounts[0], "amount": 1})


def test_cannot_pledge_if_value_does_not_match(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    with brownie.reverts():
        fundraise.pledge(amount, {"from": accounts[0], "amount": amount + 1})


def test_contributor_added_to_map_with_correct_value(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    fundraise.pledge(amount, {"from": accounts[0], "amount": amount})

    assert fundraise.amountContributed(accounts[0]) == amount


def test_contributor_map_updates_with_new_value(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount1 = (pledger_original_balance // 10) - 1
    amount2 = 1

    fundraise.pledge(amount1, {"from": accounts[0], "amount": amount1})
    fundraise.pledge(amount2, {"from": accounts[0], "amount": amount2})

    assert fundraise.amountContributed(accounts[0]) == amount1 + amount2


def test_contributor_address_added_to_array(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    fundraise.pledge(amount, {"from": accounts[0], "amount": amount})

    assert fundraise.contributors(0)
