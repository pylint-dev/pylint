"""
Example #1 of trojan unicode, see https://trojansource.codes/
Taken from https://github.com/nickboucher/trojan-source/tree/main/Python
"""


def a_function():
    """A simple function"""
    access_level = "user"
    # +1: [bidirectional-unicode]
    if access_level != "none‮⁦":  # Check if admin ⁩⁦' and access_level != 'user
        print("You are an admin.")
