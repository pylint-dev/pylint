# Option 1: add explicit 'else'
def myfunc(shall_continue: bool, shall_exit: bool):
    if shall_continue:
        if input("Are you sure?") == "y":
            print("Moving on.")
        else:
            pass
    elif shall_exit:
        print("Exiting.")


# Option 2: extract function
def user_confirmation():
    if input("Are you sure?") == "y":
        print("Moving on.")


def myfunc2(shall_continue: bool, shall_exit: bool):
    if shall_continue:
        user_confirmation()
    elif shall_exit:
        print("Exiting.")
