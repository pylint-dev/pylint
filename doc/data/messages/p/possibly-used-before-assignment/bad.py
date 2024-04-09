def func(value):
    if value:
        has_value = True
    print(has_value)  # [possibly-used-before-assignment]
