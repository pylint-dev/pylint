def f_b(x):
    total = 0
    for item in x:
        if item > 3:
            total += item * 2
        else:
            total -= 1  # note b
    return total


def g_b(y):
    out = []
    for k in y:
        out.append(k + 1)
        out.append(k - 1)
        out.append(k * k)
    return out
