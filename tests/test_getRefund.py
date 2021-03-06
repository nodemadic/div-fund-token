import brownie
from brownie import chain


def test_can_get_refund(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    fundraise.pledge(amount, {"from": accounts[0], "amount": amount})
    chain.sleep(4000)
    chain.mine()
    pledger_pre_refund_balance = accounts[0].balance()
    fundraise.getRefund({"from": accounts[0]})

    assert accounts[0].balance() > pledger_pre_refund_balance


def test_cannot_get_refund_if_token_minted(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 10

    fundraise.pledge(amount, {"from": accounts[0], "amount": (amount)})
    fundraise.closeRound({"from": accounts[0]})

    with brownie.reverts():
        fundraise.getRefund({"from": accounts[0]})


def test_cannot_get_refund_before_deadline(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    fundraise.pledge(amount, {"from": accounts[0], "amount": (amount)})

    with brownie.reverts():
        fundraise.getRefund({"from": accounts[0]})


def test_cannot_be_refunded_eth_twice(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    fundraise.pledge(amount, {"from": accounts[0], "amount": (amount)})
    chain.sleep(4000)
    chain.mine()
    fundraise.getRefund({"from": accounts[0]})
    pledger_first_refund_balance = accounts[0].balance()
    fundraise.getRefund({"from": accounts[0]})

    assert accounts[0].balance() <= pledger_first_refund_balance


def test_removes_value_from_mapping(accounts, fundraise):
    pledger_original_balance = accounts[0].balance()
    amount = (pledger_original_balance // 10) - 1

    fundraise.pledge(amount, {"from": accounts[0], "amount": (amount)})
    chain.sleep(4000)
    chain.mine()
    fundraise.getRefund({"from": accounts[0]})

    assert fundraise.amountContributed(accounts[0]) == 0
