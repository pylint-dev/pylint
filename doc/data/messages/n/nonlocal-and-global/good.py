NUMBER = 42


def create_number_updater():
    previous = None

    def update_number(number):
        global NUMBER
        NUMBER = number
        print(f"New global number is: {NUMBER}")

        nonlocal previous
        print(f"Previous global number was: {previous}")
        previous = number
    return update_number


update_number = create_number_updater()
update_number(24)
