"""
Test that no StopIteration is raised inside a generator
"""
def classic_generator(variable):
    """
    A toy generator raising StopIteration instead of using
    return statement
    """
    for i in range(variable):
        if i**3 < variable**2:
            yield i
        else:
            raise StopIteration # [stop-iteration-return]
