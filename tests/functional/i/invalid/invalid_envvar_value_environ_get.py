# pylint: disable=missing-docstring
"""Regression test for invalid-envvar-default/value on os.environ.get.

os.environ.get(key[, default]) has the same semantics as os.getenv.
See https://github.com/pylint-dev/pylint/issues/10092
"""
import os


def _returns_bytes():
    return b"bytes"


def _returns_list():
    return []


def _returns_none():
    return None


def _returns_str():
    return "string"


# key argument checks
os.environ.get(b"TEST")  # [invalid-envvar-value]
os.environ.get("TEST")
os.environ.get(None)  # [invalid-envvar-value]
os.environ.get(["list"])  # [invalid-envvar-value]
os.environ.get(_returns_bytes())  # [invalid-envvar-value]
os.environ.get(_returns_str())

# default argument checks
os.environ.get("TEST", "value")
os.environ.get("TEST", None)
os.environ.get("TEST", [])  # [invalid-envvar-default]
os.environ.get("TEST", b"123")  # [invalid-envvar-default]
os.environ.get("TEST", _returns_list())  # [invalid-envvar-default]
os.environ.get("TEST", _returns_none())
os.environ.get("TEST", _returns_str())
os.environ.get("TEST", _returns_bytes())  # [invalid-envvar-default]

# keyword argument variants
os.environ.get(key="TEST")
os.environ.get(key="TEST", default="value")
os.environ.get(key="TEST", default=[])  # [invalid-envvar-default]
os.environ.get(key="TEST", default=b"bytes")  # [invalid-envvar-default]
