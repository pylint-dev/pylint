def divide_x_by_y(x: float, y: float):
    try:
        print(x / y)
    except FloatingPointError as e:
        print(f"There was a FloatingPointError: {e}")
    except ArithmeticError as e:
        # FloatingPointError  were already caught at this point
        print(f"There was an OverflowError or a ZeroDivisionError: {e}")

Or:

def divide_x_by_y(x: float, y: float):
    try:
        print(x / y)
    except ArithmeticError as e:
        print(f"There was an OverflowError, a ZeroDivisionError or a FloatingPointError : {e}")
