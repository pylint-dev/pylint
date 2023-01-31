def foo():
    # McCabe rating is 11 here (by default 10)
    # +1: [too-complex]
    myint = 2
    if myint == 5:
        return myint
    elif myint == 6:
        return myint
    elif myint == 7:
        return myint
    elif myint == 8:
        return myint
    elif myint == 9:
        return myint
    elif myint == 10:
        if myint == 8:
            while True:
                return True
        elif myint == 8:
            with myint:
                return 8
    else:
        if myint == 2:
            return myint
        return myint
    return myint