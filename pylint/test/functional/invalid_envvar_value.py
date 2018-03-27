# pylint: disable=useless-return,missing-docstring
from os import getenv


def function_returning_list():
    return []

def function_returning_none():
    return None

def function_returning_string():
    return "Result"

def function_returning_bytes():
    return b"Result"

def deep_function_returning_string():
    return function_returning_string()

def deep_function_returning_bytes():
    return function_returning_bytes()


# --------------------------------------------------------------------------- #
#                               Testing getenv                                #
# --------------------------------------------------------------------------- #

getenv()   # pylint: disable=no-value-for-parameter

getenv(b"TEST")  # [invalid-envvar-value]
getenv("TEST")
getenv(None)   # [invalid-envvar-value]
getenv(["Crap"])   # [invalid-envvar-value]
getenv(function_returning_bytes())   # [invalid-envvar-value]
getenv(deep_function_returning_bytes())   # [invalid-envvar-value]
getenv(function_returning_list())   # [invalid-envvar-value]
getenv(function_returning_none())   # [invalid-envvar-value]
getenv(function_returning_string())
getenv(deep_function_returning_string())

getenv(b"TEST", "default")   # [invalid-envvar-value]
getenv("TEST", "default")
getenv(None, "default")  # [invalid-envvar-value]
getenv(["Crap"], "default")   # [invalid-envvar-value]
getenv(function_returning_bytes(), "default")   # [invalid-envvar-value]
getenv(function_returning_list(), "default")   # [invalid-envvar-value]
getenv(function_returning_none(), "default")   # [invalid-envvar-value]
getenv(function_returning_string(), "default")

getenv(key=b"TEST")   # [invalid-envvar-value]
getenv(key="TEST")
getenv(key=None)    # [invalid-envvar-value]
getenv(key=["Crap"])   # [invalid-envvar-value]
getenv(key=function_returning_bytes())   # [invalid-envvar-value]
getenv(key=function_returning_list())   # [invalid-envvar-value]
getenv(key=function_returning_none())   # [invalid-envvar-value]
getenv(key=function_returning_string())

getenv('TEST', "value")
getenv('TEST', [])  # [invalid-envvar-default]
getenv('TEST', None)
getenv('TEST', b"123")  # [invalid-envvar-default]
getenv('TEST', function_returning_list()) # [invalid-envvar-default]
getenv('TEST', function_returning_none())
getenv('TEST', function_returning_string())
getenv('TEST', function_returning_bytes())   # [invalid-envvar-default]

getenv('TEST', default="value")
getenv('TEST', default=[])  # [invalid-envvar-default]
getenv('TEST', default=None)
getenv('TEST', default=b"123")  # [invalid-envvar-default]
getenv('TEST', default=function_returning_list())  # [invalid-envvar-default]
getenv('TEST', default=function_returning_none())
getenv('TEST', default=function_returning_string())
getenv('TEST', default=function_returning_bytes())  # [invalid-envvar-default]

getenv(key='TEST')
getenv(key='TEST', default="value")
getenv(key='TEST', default=b"value")  # [invalid-envvar-default]
getenv(key='TEST', default=["Crap"])  # [invalid-envvar-default]
getenv(key='TEST', default=function_returning_list())  # [invalid-envvar-default]
getenv(key='TEST', default=function_returning_none())
getenv(key='TEST', default=function_returning_string())
getenv(key='TEST', default=function_returning_bytes())  # [invalid-envvar-default]
