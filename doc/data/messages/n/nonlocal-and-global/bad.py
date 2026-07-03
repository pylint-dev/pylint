NUMBER = 42


def update_number(number):  # [nonlocal-and-global]
    global NUMBER
    nonlocal NUMBER
    NUMBER = number
    print(f"New global number is: {NUMBER}")


update_number(24)
