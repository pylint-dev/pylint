def important_math(x: int, y: int) -> None:
    if x == 0:  # [use-implicit-booleaness-not-comparison-to-zero]
        print("x is equal to zero")

    if y != 0:  # [use-implicit-booleaness-not-comparison-to-zero]
        print("y is not equal to zero")
