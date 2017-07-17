"""
Test that no StopIteration is raised inside a generator
"""
class RebornStopIteration(StopIteration):
    """
    A class inheriting from StopIteration exception
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

def generator_non_std_exc_raising(variable):
    """
    A toy generator raising non standard exception inheriting from
    StopIteration instead of using return statement
    """
    for i in range(variable):
        if i**3 < variable**2:
            yield i
        else:
            raise RebornStopIteration # [stop-iteration-return]
