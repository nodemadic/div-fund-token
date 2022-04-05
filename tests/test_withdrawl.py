# #!/usr/bin/python3
# import brownie


def test_withdrawer_balance_increases(accounts, token):
    withdrawer_balance = accounts[0].balance()
    depositer_balance = accounts[1].balance()
    amount = depositer_balance // 4

    token.deposit({"from": accounts[1], "amount": amount})
    token.withdraw({"from": accounts[0]})

    assert withdrawer_balance < accounts[0].balance()


def test_withdrawer_balance_doesnt_increase(accounts, token):
    withdrawer_balance = accounts[0].balance()
    depositer_balance = accounts[1].balance()
    amount = depositer_balance // 4

    token.withdraw({"from": accounts[0]})
    token.deposit({"from": accounts[1], "amount": amount})

    assert withdrawer_balance >= accounts[0].balance()
