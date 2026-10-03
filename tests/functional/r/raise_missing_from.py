# pylint:disable=missing-docstring, unreachable, using-constant-test, invalid-name, bare-except
# pylint:disable=try-except-raise, undefined-variable, too-few-public-methods, superfluous-parens, no-else-raise

try:
    1 / 0
except:
    raise ValueError('Invalid integer')  # [raise-missing-from]

try:
    1 / 0
except ZeroDivisionError:
    # +1: [raise-missing-from]
    raise KeyError

try:
    1 / 0
except ZeroDivisionError:
    # Our algorithm doesn't have to be careful about the complicated expression below,
    # because the exception above wasn't bound to a name. # +1: [raise-missing-from]
    raise (foo + bar).baz

try:
    1 / 0
except ZeroDivisionError as e:
    # +1: [raise-missing-from]
    raise KeyError

try:
    1 / 0
except ZeroDivisionError as e:
    # +1: [raise-missing-from]
    raise KeyError
else:
    pass
finally:
    pass

try:
    1 / 0
except ZeroDivisionError as e:
    if 1:
        if 1:
            with whatever:
                try:
                    # +1: [raise-missing-from]
                    raise KeyError
                except:
                    pass

try:
    1 / 0
except ZeroDivisionError as e:
    # +1: [raise-missing-from]
    raise KeyError()

try:
    1 / 0
except ZeroDivisionError as e:
    # +1: [raise-missing-from]
    raise KeyError(whatever, whatever=whatever)


try:
    1 / 0
except (ZeroDivisionError, ValueError, KeyError):
    if 1:
        if 2:
            pass
        else:
            with whatever:
                # +1: [raise-missing-from]
                raise KeyError(whatever, whatever=whatever)
    else:
        # +1: [raise-missing-from]
        raise KeyError(whatever, overever=12)

try:
    # Taken from https://github.com/python/cpython/blob/3.10/Lib/plistlib.py#L459
    pass
except (OSError, IndexError, struct.error, OverflowError,
        ValueError):
    raise InvalidFileException()  # [raise-missing-from]

try:
    1 / 0
except ZeroDivisionError:
    raise KeyError from foo

try:
    1 / 0
except ZeroDivisionError:
    raise (foo + bar).baz from foo

try:
    1 / 0
except ZeroDivisionError as e:
    raise KeyError from foo

try:
    1 / 0
except ZeroDivisionError as e:
    raise KeyError from foo
else:
    pass
finally:
    pass

try:
    1 / 0
except ZeroDivisionError as e:
    if 1:
        if 1:
            with whatever:
                try:
                    raise KeyError from foo
                except:
                    pass

try:
    1 / 0
except ZeroDivisionError as e:
    raise KeyError() from foo

try:
    1 / 0
except ZeroDivisionError as e:
    raise KeyError(whatever, whatever=whatever) from foo

try:
    1 / 0
except ZeroDivisionError:
    raise

try:
    1 / 0
except ZeroDivisionError as e:
    raise

try:
    1 / 0
except ZeroDivisionError as e:
    raise e

try:
    1 / 0
except ZeroDivisionError as e:
    if 1:
        if 1:
            if 1:
                raise e

try:
    1 / 0
except ZeroDivisionError as e:
    raise e.with_traceback(e.__traceback__)

try:
    1 / 0
except ZeroDivisionError as e:
    raise (e + 7)

try:
    1 / 0
except ZeroDivisionError as e:
    def f():
        raise KeyError

try:
    1 / 0
except ZeroDivisionError as e:
    class Foo:
        raise KeyError
