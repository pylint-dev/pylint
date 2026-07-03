def get_max(value1, value2):
    if value1 < value2:  # [consider-using-max-builtin]
        value1 = value2
    return value1


print(get_max(1, 2))
