# pylint: disable=invalid-name,missing-docstring,pointless-statement
from datetime import datetime
from typing import Union

value = "Hello World"
value.isoformat()  # [no-member]


if isinstance(value, datetime):
    value.isoformat()
else:
    value.isoformat()  # [no-member]


def func():
    if hasattr(value, "load"):
        value.load()

    if getattr(value, "load", None):
        value.load


if value.none_existent():  # [no-member]
    pass

res = value.isoformat() if isinstance(value, datetime) else value


class Base:
    _attr_state: Union[str, datetime] = "Unknown"

    @property
    def state(self) -> Union[str, datetime]:
        return self._attr_state

    def some_function(self) -> str:
        state = self.state
        if isinstance(state, datetime):
            return state.isoformat()
        return str(state)


# https://github.com/pylint-dev/pylint/issues/1990
# Attribute access after 'isinstance' should not cause 'no-member' error
import subprocess  # pylint: disable=wrong-import-position  # noqa: E402

try:
    subprocess.check_call(['ls', '-'])  # Deliberately made error in this line
except Exception as err:
    if isinstance(err, subprocess.CalledProcessError):
        print(f'Subprocess error occurred. Return code: {err.returncode}')
    else:
        print(f'An error occurred: {str(err)}')
    raise


# https://github.com/pylint-dev/pylint/issues/4168
# 'encode' for 'arg' should not cause 'no-member' error
mixed_tuple = (b"a", b"b", b"c", b"d")
byte_tuple = [arg.encode('utf8') if isinstance(arg, str) else arg for arg in mixed_tuple]

for arg in mixed_tuple:
    if isinstance(arg, str):
        print(arg.encode('utf8'))
    else:
        print(arg)


# https://github.com/pylint-dev/pylint/issues/1162
# Attribute access after 'isinstance' should not cause 'no-member' error
class FoobarException(Exception):
    foobar = None

try:  # noqa: E305
    pass
except Exception as ex:
    if isinstance(ex, FoobarException):
        ex.foobar
    raise
