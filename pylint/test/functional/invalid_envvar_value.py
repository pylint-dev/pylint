import os
from os import environ, getenv, putenv


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

getenv()

getenv(b"TEST")
getenv("TEST")
getenv(None)
getenv(["Crap"])
getenv(function_returning_bytes())
getenv(deep_function_returning_bytes())
getenv(function_returning_list())
getenv(function_returning_none())
getenv(function_returning_string())
getenv(deep_function_returning_string())

getenv(b"TEST", "default")
getenv("TEST", "default")
getenv(None, "default")
getenv(["Crap"], "default")
getenv(function_returning_bytes(), "default")
getenv(function_returning_list(), "default")
getenv(function_returning_none(), "default")
getenv(function_returning_string(), "default")

getenv(key=b"TEST")
getenv(key="TEST")
getenv(key=None)
getenv(key=["Crap"])
getenv(key=function_returning_bytes())
getenv(key=function_returning_list())
getenv(key=function_returning_none())
getenv(key=function_returning_string())

getenv('TEST', "value")
getenv('TEST', [])
getenv('TEST', None)
getenv('TEST', b"123")
getenv('TEST', function_returning_list())
getenv('TEST', function_returning_none())
getenv('TEST', function_returning_string())
getenv('TEST', function_returning_bytes())

getenv('TEST', default="value")
getenv('TEST', default=[])
getenv('TEST', default=None)
getenv('TEST', default=b"123")
getenv('TEST', default=function_returning_list())
getenv('TEST', default=function_returning_none())
getenv('TEST', default=function_returning_string())
getenv('TEST', default=function_returning_bytes())

getenv(key='TEST')
getenv(key='TEST', default="value")
getenv(key='TEST', default=b"value")
getenv(key='TEST', default=["Crap"])
getenv(key='TEST', default=function_returning_list())
getenv(key='TEST', default=function_returning_none())
getenv(key='TEST', default=function_returning_string())
getenv(key='TEST', default=function_returning_bytes())


# --------------------------------------------------------------------------- #
#                                 Test putenv                                 #
# --------------------------------------------------------------------------- #

putenv()

putenv(b"TEST")
putenv("TEST")
putenv(None)
putenv(["Crap"])
putenv(function_returning_bytes())
putenv(function_returning_list())
putenv(function_returning_none())
putenv(function_returning_string())

putenv(b"TEST", "default")
putenv("TEST", "default")
putenv(None, "default")
putenv(["Crap"], "default")
putenv(function_returning_bytes(), "default")
putenv(function_returning_list(), "default")
putenv(function_returning_none(), "default")
putenv(function_returning_string(), "default")

putenv(key=b"TEST")
putenv(key="TEST")
putenv(key=None)
putenv(key=["Crap"])
putenv(key=function_returning_bytes())
putenv(key=function_returning_list())
putenv(key=function_returning_none())
putenv(key=function_returning_string())

putenv('TEST', "value")
putenv('TEST', [])
putenv('TEST', None)
putenv('TEST', b"123")
putenv('TEST', function_returning_list())
putenv('TEST', function_returning_none())
putenv('TEST', function_returning_string())
putenv('TEST', function_returning_bytes())

putenv('TEST', default="value")
putenv('TEST', default=[])
putenv('TEST', default=None)
putenv('TEST', default=b"123")
putenv('TEST', default=function_returning_list())
putenv('TEST', default=function_returning_none())
putenv('TEST', default=function_returning_string())
putenv('TEST', default=function_returning_bytes())

putenv(key='TEST')
putenv(key='TEST', default="value")
putenv(key='TEST', default=b"value")
putenv(key='TEST', default=["Crap"])
putenv(key='TEST', default=function_returning_list())
putenv(key='TEST', default=function_returning_none())
putenv(key='TEST', default=function_returning_string())
putenv(key='TEST', default=function_returning_bytes())
