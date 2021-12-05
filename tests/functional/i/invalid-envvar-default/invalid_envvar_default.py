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


getenv("TEST", "value")
getenv("TEST", [])  # [invalid-envvar-default]
getenv("TEST", None)
getenv("TEST", b"123")  # [invalid-envvar-default]
getenv("TEST", function_returning_list())  # [invalid-envvar-default]
getenv("TEST", function_returning_none())
getenv("TEST", function_returning_string())
getenv("TEST", function_returning_bytes())  # [invalid-envvar-default]

getenv("TEST", default="value")
getenv("TEST", default=[])  # [invalid-envvar-default]
getenv("TEST", default=None)
getenv("TEST", default=b"123")  # [invalid-envvar-default]
getenv("TEST", default=function_returning_list())  # [invalid-envvar-default]
getenv("TEST", default=function_returning_none())
getenv("TEST", default=function_returning_string())
getenv("TEST", default=function_returning_bytes())  # [invalid-envvar-default]

getenv(key="TEST")
getenv(key="TEST", default="value")
getenv(key="TEST", default=b"value")  # [invalid-envvar-default]
getenv(key="TEST", default=["Crap"])  # [invalid-envvar-default]
getenv(key="TEST", default=function_returning_list())  # [invalid-envvar-default]
getenv(key="TEST", default=function_returning_none())
getenv(key="TEST", default=function_returning_string())
getenv(key="TEST", default=function_returning_bytes())  # [invalid-envvar-default]
