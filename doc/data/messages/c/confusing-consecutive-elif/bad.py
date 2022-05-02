def myfunc(shall_continue: bool, shall_exit: bool):
    if shall_continue:
        if input("Are you sure?") == "y":
            print("Moving on.")
    elif shall_exit:  # [confusing-consecutive-elif]
        print("Exiting.")
