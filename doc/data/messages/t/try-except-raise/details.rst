There is a legitimate use case for re-raising immediately. E.g. with the following inheritance tree::

    +-- ArithmeticError
         +-- FloatingPointError
         +-- OverflowError
         +-- ZeroDivisionError

The following code shows valid case for re-raising exception immediately::

    def execute_calculation(a, b):
        try:
            return some_calculation(a, b)
        except ZeroDivisionError:
            raise
        except ArithmeticError:
            return float('nan')

The pylint is able to detect this case and does not produce error.
