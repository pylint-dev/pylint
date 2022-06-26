def foo(x, y, z):
    if all([x, y, z]) and set(map(lambda n: n % 2, [x, y, z])).issubset({0}):
        pass
