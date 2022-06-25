def fruit(value):
    try:
        return 2 / value
    except ZeroDivisionError:
        print('Connot divide zero.')

    return 0
