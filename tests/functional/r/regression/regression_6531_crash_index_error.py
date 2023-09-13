"""Regression test for https://github.com/pylint-dev/pylint/issues/6531."""

# pylint: disable=missing-docstring, redefined-outer-name

import pytest


class Wallet:
    def __init__(self):
        self.balance = 0

    def add_cash(self, earned):
        self.balance += earned

    def spend_cash(self, spent):
        self.balance -= spent

@pytest.fixture
def my_wallet():
    '''Returns a Wallet instance with a zero balance'''
    return Wallet()

@pytest.mark.parametrize("earned,spent,expected", [
    (30, 10, 20),
    (20, 2, 18),
])
def test_transactions(my_wallet, earned, spent, expected):
    my_wallet.add_cash(earned)
    my_wallet.spend_cash(spent)
    assert my_wallet.balance == expected
