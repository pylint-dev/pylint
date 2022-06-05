def divide_x_by_y(x: float, y: float):
    try:
        print(x / y)
    except (ArithmeticError, FloatingPointError) as e:  # [overlapping-except]
        print(f"There was an issue: {e}")
