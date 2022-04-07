import brownie
from brownie import chain


def test_can_get_refund(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 16

    token.pledge(amount, {"from": accounts[0], "amount": amount})
    chain.sleep(4000)
    chain.mine()
    pledger_pre_refund_balance = accounts[0].balance()
    token.getRefund({"from": accounts[0]})

    assert accounts[0].balance() > pledger_pre_refund_balance


def test_cannot_get_refund_if_token_minted(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount1 = pledger_original_balance // 16
    amount2 = pledger_original_balance // 4

    token.pledge(amount1, {"from": accounts[0], "amount": (amount1)})
    token.pledge(amount2, {"from": accounts[1], "amount": (amount2)})
    token.closeRound({"from": accounts[0]})

    with brownie.reverts():
        token.getRefund({"from": accounts[0]})


def test_cannot_get_refund_before_deadline(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 16

    token.pledge(amount, {"from": accounts[0], "amount": (amount)})

    with brownie.reverts():
        token.getRefund({"from": accounts[0]})


def test_cannot_be_refunded_eth_twice(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 16

    token.pledge(amount, {"from": accounts[0], "amount": (amount)})
    chain.sleep(4000)
    chain.mine()
    token.getRefund({"from": accounts[0]})
    pledger_first_refund_balance = accounts[0].balance()
    token.getRefund({"from": accounts[0]})

    assert accounts[0].balance() <= pledger_first_refund_balance


def test_removes_value_from_mapping(accounts, token):
    pledger_original_balance = accounts[0].balance()
    amount = pledger_original_balance // 16

    token.pledge(amount, {"from": accounts[0], "amount": (amount)})
    chain.sleep(4000)
    chain.mine()
    token.getRefund({"from": accounts[0]})

    assert token.amountContributed(accounts[0]) == 0
