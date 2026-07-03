def get_min(value1, value2):
    if value1 > value2:  # [consider-using-min-builtin]
        value1 = value2
    return value1


print(get_min(1, 2))
