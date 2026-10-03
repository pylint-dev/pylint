def check_lunchbox(items: list[str]):
    if not items:
        empty = True
    print(empty)  # [possibly-used-before-assignment]
