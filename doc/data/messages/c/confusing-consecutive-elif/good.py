def myfunc(shall_continue: bool, shall_exit: bool):
    if shall_continue:
        if input("Are you sure?") == "y":
            print("Moving on.")
        else:
            pass
    elif shall_exit:
        print("Exiting.")
