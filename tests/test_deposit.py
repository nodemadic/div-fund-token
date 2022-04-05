#!/usr/bin/python3
import brownie
from dotenv import load_dotenv
import os

load_dotenv()


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


def test_dividend_per_token_increases(accounts, token):
    depositer_original_balance = accounts[0].balance()
    amount = depositer_original_balance // 4
    scaled_dividend_per_token_original_amount = token.scaledDividendPerToken()

    token.deposit({"from": accounts[0], "amount": amount})

    assert scaled_dividend_per_token_original_amount < token.scaledDividendPerToken()


def test_dividend_per_token_increases_by_proportional_amount(accounts, token):
    depositer_original_balance = accounts[0].balance()
    amount = depositer_original_balance // 4
    scaled_dividend_per_token_original_amount = token.scaledDividendPerToken()

    token.deposit({"from": accounts[0], "amount": amount})

    total_change = (amount * token.scaling()) + token.scaledRemainder()
    per_token_change = total_change / token.totalSupply()
    scaled_dividend_per_token_current_amount = token.scaledDividendPerToken()

    assert (
        scaled_dividend_per_token_original_amount + per_token_change
        == scaled_dividend_per_token_current_amount
    )


def test_scaled_remainder_is_adjusted(accounts, token):
    depositer_original_balance = accounts[0].balance()
    amount = depositer_original_balance / float(os.getenv("PI_VALUE"))
    scaled_remainder_original_amount = token.scaledRemainder()

    token.transfer(accounts[1], 1, {"from": accounts[0]})
    token.deposit({"from": accounts[0], "amount": amount})

    # This needs to be changed to work later
    assert token.scaledRemainder() == scaled_remainder_original_amount
