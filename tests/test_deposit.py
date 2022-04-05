#!/usr/bin/python3
import brownie


def test_depositer_balance_decreases(accounts, token):
    depositer_original_balance = accounts[0].balance()
    amount = depositer_original_balance // 4

    token.deposit({"from": accounts[0], "amount": amount})

    assert accounts[0].balance() >= depositer_original_balance - amount


def test_contract_balance_increases_by_amound_deposited(accounts, token):
    contract_original_balance = token.balance()
    depositer_original_balance = accounts[0].balance()
    amount = depositer_original_balance // 4

    token.deposit({"from": accounts[0], "amount": amount})

    assert token.balance() == contract_original_balance + amount
