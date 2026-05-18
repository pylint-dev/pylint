def divide_x_by_y(x: float, y: float):
    try:
        print(x / y)
    except ArithmeticError as e:
        print(
            f"There was an OverflowError, a ZeroDivisionError or a FloatingPointError: {e}"
        )
