#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(TestDividendTokenERC20, accounts):
    return TestDividendTokenERC20.deploy(
        "TDividend",
        "TDIV",
        {"from": accounts[0]},
    )


@pytest.fixture(scope="module")
def fundraise(Fundraise, accounts):
    return Fundraise.deploy(
        accounts[1],
        "Dividend",
        "DIV",
        1,
        10000000000000000000,
        {"from": accounts[0]},
    )


@pytest.fixture(scope="module")
def nft(MyToken, accounts):
    return MyToken.deploy(
        {"from": accounts[0]},
    )


@pytest.fixture(scope="module")
def listings(Listings, accounts):
    return Listings.deploy(
        {"from": accounts[0]},
    )
