# pylint: disable=useless-return,missing-docstring
import os
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
int(getenv("TEST", 1))
float(getenv("TEST", 1.0))
getenv('TEST', [])  # [invalid-envvar-default]
getenv('TEST', None)
getenv('TEST', b"123")  # [invalid-envvar-default]
getenv('TEST', function_returning_list()) # [invalid-envvar-default]
getenv('TEST', function_returning_none())
getenv('TEST', function_returning_string())
getenv('TEST', function_returning_bytes())   # [invalid-envvar-default]

getenv('TEST', default="value")
int(getenv("TEST", default=1))
float(getenv("TEST", default=1.0))
getenv('TEST', default=[])  # [invalid-envvar-default]
getenv('TEST', default=None)
getenv('TEST', default=b"123")  # [invalid-envvar-default]
getenv('TEST', default=function_returning_list())  # [invalid-envvar-default]
getenv('TEST', default=function_returning_none())
getenv('TEST', default=function_returning_string())
getenv('TEST', default=function_returning_bytes())  # [invalid-envvar-default]

getenv(key='TEST')
getenv(key='TEST', default="value")
int(getenv(key="TEST", default=1))
float(getenv(key="TEST", default=1.0))
getenv(key='TEST', default=b"value")  # [invalid-envvar-default]
getenv(key='TEST', default=["Crap"])  # [invalid-envvar-default]
getenv(key='TEST', default=function_returning_list())  # [invalid-envvar-default]
getenv(key='TEST', default=function_returning_none())
getenv(key='TEST', default=function_returning_string())
getenv(key='TEST', default=function_returning_bytes())  # [invalid-envvar-default]

os.environ.get()   # pylint: disable=no-value-for-parameter

os.environ.get(b"TEST")  # [invalid-envvar-value]
os.environ.get("TEST")
os.environ.get(None)   # [invalid-envvar-value]
os.environ.get(["Crap"])   # [invalid-envvar-value]
os.environ.get(function_returning_bytes())   # [invalid-envvar-value]
os.environ.get(deep_function_returning_bytes())   # [invalid-envvar-value]
os.environ.get(function_returning_list())   # [invalid-envvar-value]
os.environ.get(function_returning_none())   # [invalid-envvar-value]
os.environ.get(function_returning_string())
os.environ.get(deep_function_returning_string())

os.environ.get(b"TEST", "default")   # [invalid-envvar-value]
os.environ.get("TEST", "default")
os.environ.get(None, "default")  # [invalid-envvar-value]
os.environ.get(["Crap"], "default")   # [invalid-envvar-value]
os.environ.get(function_returning_bytes(), "default")   # [invalid-envvar-value]
os.environ.get(function_returning_list(), "default")   # [invalid-envvar-value]
os.environ.get(function_returning_none(), "default")   # [invalid-envvar-value]
os.environ.get(function_returning_string(), "default")

os.environ.get(key=b"TEST")   # [invalid-envvar-value]
os.environ.get(key="TEST")
os.environ.get(key=None)    # [invalid-envvar-value]
os.environ.get(key=["Crap"])   # [invalid-envvar-value]
os.environ.get(key=function_returning_bytes())   # [invalid-envvar-value]
os.environ.get(key=function_returning_list())   # [invalid-envvar-value]
os.environ.get(key=function_returning_none())   # [invalid-envvar-value]
os.environ.get(key=function_returning_string())

os.environ.get('TEST', "value")
int(os.environ.get("TEST", 1))
float(os.environ.get("TEST", 1.0))
os.environ.get('TEST', [])  # [invalid-envvar-default]
os.environ.get('TEST', None)
os.environ.get('TEST', b"123")  # [invalid-envvar-default]
os.environ.get('TEST', function_returning_list()) # [invalid-envvar-default]
os.environ.get('TEST', function_returning_none())
os.environ.get('TEST', function_returning_string())
os.environ.get('TEST', function_returning_bytes())   # [invalid-envvar-default]

os.environ.get('TEST', default="value")
int(os.environ.get("TEST", default=1))
float(os.environ.get("TEST", default=1.0))
os.environ.get('TEST', default=[])  # [invalid-envvar-default]
os.environ.get('TEST', default=None)
os.environ.get('TEST', default=b"123")  # [invalid-envvar-default]
os.environ.get('TEST', default=function_returning_list())  # [invalid-envvar-default]
os.environ.get('TEST', default=function_returning_none())
os.environ.get('TEST', default=function_returning_string())
os.environ.get('TEST', default=function_returning_bytes())  # [invalid-envvar-default]

os.environ.get(key='TEST')
os.environ.get(key='TEST', default="value")
int(os.environ.get(key="TEST", default=1))
float(os.environ.get(key="TEST", default=1.0))
os.environ.get(key='TEST', default=b"value")  # [invalid-envvar-default]
os.environ.get(key='TEST', default=["Crap"])  # [invalid-envvar-default]
os.environ.get(key='TEST', default=function_returning_list())  # [invalid-envvar-default]
os.environ.get(key='TEST', default=function_returning_none())
os.environ.get(key='TEST', default=function_returning_string())
os.environ.get(key='TEST', default=function_returning_bytes())  # [invalid-envvar-default]
os.environ.get(key='TEST', default=function_returning_bytes())  # [invalid-envvar-default]
