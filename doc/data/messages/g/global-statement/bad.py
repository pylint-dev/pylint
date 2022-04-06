price = 25


def add_cost():
    global price  # [global-statement]
    price = price + 10
    return price
