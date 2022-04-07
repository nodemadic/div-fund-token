import brownie
from brownie import chain


def test_can_pledge_before_deadline(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 4

    token.pledge(amount, {"from": accounts[0], "amount": amount})

    assert accounts[0].balance() <= pledger_original_balance - amount


def test_cannot_pledge_after_deadline(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 4

    chain.sleep(4000)
    chain.mine()

    with brownie.reverts():
        token.pledge(amount, {"from": accounts[0], "amount": amount})


# Must wait for future functions to be tested
def test_cannot_pledge_if_token_already_minted(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 4

    token.pledge(amount, {"from": accounts[1], "amount": (amount)})
    token.closeRound({"from": accounts[0]})

    with brownie.reverts():
        token.pledge((amount // 100000), {"from": accounts[0], "amount": amount})


def test_cannot_pledge_if_already_raised_enough(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 4

    token.pledge(amount, {"from": accounts[1], "amount": (amount)})

    with brownie.reverts():
        token.pledge(amount, {"from": accounts[0], "amount": amount})


def test_cannot_pledge_if_value_does_not_match(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 4

    with brownie.reverts():
        token.pledge(amount, {"from": accounts[0], "amount": amount + 1})


def test_contributor_added_to_map_with_correct_value(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 4

    token.pledge(amount, {"from": accounts[0], "amount": amount})

    assert token.amountContributed(accounts[0]) == amount


def test_contributor_map_updates_with_new_value(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount1 = pledger_original_balance // 16
    amount2 = pledger_original_balance // 4

    token.pledge(amount1, {"from": accounts[0], "amount": amount1})
    token.pledge(amount2, {"from": accounts[0], "amount": amount2})

    assert token.amountContributed(accounts[0]) == amount1 + amount2


def test_contributor_address_added_to_array(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 4

    token.pledge(amount, {"from": accounts[0], "amount": amount})

    assert token.contributors(0)
