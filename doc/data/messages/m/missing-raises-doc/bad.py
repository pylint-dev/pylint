def integer_sum(a, b):  # [missing-raises-doc]
    """Returns sum of two integers
    :param a: first integer
    :type a: int
    :param b: second integer
    :type b: int
    """
    if not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError('Function supports only integer parameters.')
    return a + b
