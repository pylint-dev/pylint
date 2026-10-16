def describe_number(value: int | None) -> str:
    if value is None:
        return "missing"
    if value < 0:
        description = "negative"
    elif value == 0:
        return "zero"
    else:
        description = "positive"
    return description
