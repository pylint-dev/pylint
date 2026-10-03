def integer_sum(a: int, b: int) -> int:
    if not (isinstance(a, int) and isinstance(b, int)):  # [no-else-raise]
        raise ValueError("Function supports only integer parameters.")
    else:
        return a + b
