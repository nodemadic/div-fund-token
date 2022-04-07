#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(Fundraise, accounts):
    return Fundraise.deploy(
        accounts[1],
        "Dividend",
        "DIV",
        1,
        50000000000000000000,
        {"from": accounts[0]},
    )
