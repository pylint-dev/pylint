def print_all(*values, sep=" "):
    print(*values, sep=sep)


print_all(sep=", ", *["apple", "banana"])  # [star-arg-unpacking-after-keyword-arg]
