def small_apple(apple, length):
    if len(apple) < length:
        raise IndexError("Apple is too small!")
    print(f"{apple} is proper size.")
