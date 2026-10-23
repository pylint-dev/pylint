def f_c(x):
    total = 0
    for item in x:
        if item > 3:
            total += item * 2
        else:
            total -= 1  # note c
    return total


def g_c(y):
    out = []
    for k in y:
        out.append(k + 1)
        out.append(k - 1)
        out.append(k * k)
    return out
