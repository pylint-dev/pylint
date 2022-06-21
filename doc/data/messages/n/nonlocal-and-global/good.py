NUMBER = 42


def update_number(number):
    global NUMBER
    NUMBER = number
    print(f"New global number is: {NUMBER}")


update_number(24)
