"""
Example #2 of trojan unicode, see https://trojansource.codes/
Taken from https://github.com/nickboucher/trojan-source/tree/main/Python
"""
# pylint: disable=unreachable

bank = {"alice": 100}

# +4: [bidirectional-unicode]


def subtract_funds(account: str, amount: int):
    """Subtract funds from bank account then ⁧"""
    return
    bank[account] -= amount
    return


subtract_funds("alice", 50)
