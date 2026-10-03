def validate_positive(x):
    if x <= 0:
        raise ValueError(f"{x} is not positive")
