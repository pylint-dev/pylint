def integer_sum(a: int, b: int) -> int:
    if not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError("Function supports only integer parameters.")
    return a + b
