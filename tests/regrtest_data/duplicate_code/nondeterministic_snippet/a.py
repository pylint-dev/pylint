def f_a(x):
    total = 0
    for item in x:
        if item > 3:
            total += item * 2
        else:
            total -= 1  # note a
    return total


def g_a(y):
    out = []
    for k in y:
        out.append(k + 1)
        out.append(k - 1)
        out.append(k * k)
    return out
