def small_apple(apple, length):
    if len(apple) < length:
        raise Exception("Apple is too small!")  # [broad-exception-raised]
    print(f"{apple} is proper size.")
