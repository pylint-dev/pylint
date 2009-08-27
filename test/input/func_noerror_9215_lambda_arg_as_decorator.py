"""Demonstrate false undefined variable for lambda functions.

http://www.logilab.org/ticket/9215
"""

__revision__ = None

def decorator(expr):
    """Function returning decorator."""
    def func(function):
        """Pass-thru decorator."""
        return function
    # use expr
    expr(0)
    return func

# this lambda is flagged
# E0602:  16:main.<lambda>: Undefined variable 'x'
@decorator(lambda x: x > 0)
def main():
    """Dummy function."""
    # this one is not flagged
    decorator(lambda y: y > 0)

if __name__ == "__main__":
    main()



