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

def generator_stopiter_catched(variable):
    """
    A toy generator raising StopIteration that is catched inside
    a try/except block
    """
    for i in range(variable):
        if i**3 < variable**2:
            yield i
        else:
            try:
                raise StopIteration
            except StopIteration:
                return

def generator_stopiter_notcatched(variable):
    """
    A toy generator raising StopIteration that is nested inside
    a try/except bloc but the latter does not handle it
    """
    for i in range(variable):
        if i**3 < variable**2:
            yield i
        else:
            try:
                raise StopIteration # [stop-iteration-return]
            except ValueError:
                return
