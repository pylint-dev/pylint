"""Tests for missing-timeout."""

# pylint: disable=consider-using-with,import-error,no-member,no-name-in-module,reimported

import requests
from requests import (
    delete,
    delete as delete_r,
    get,
    get as get_r,
    head,
    head as head_r,
    options,
    options as options_r,
    patch,
    patch as patch_r,
    post,
    post as post_r,
    put,
    put as put_r,
    request,
    request as request_r,
)

# requests without timeout
requests.delete("http://localhost")  # [missing-timeout]
requests.get("http://localhost")  # [missing-timeout]
requests.head("http://localhost")  # [missing-timeout]
requests.options("http://localhost")  # [missing-timeout]
requests.patch("http://localhost")  # [missing-timeout]
requests.post("http://localhost")  # [missing-timeout]
requests.put("http://localhost")  # [missing-timeout]
requests.request("call", "http://localhost")  # [missing-timeout]

delete_r("http://localhost")  # [missing-timeout]
get_r("http://localhost")  # [missing-timeout]
head_r("http://localhost")  # [missing-timeout]
options_r("http://localhost")  # [missing-timeout]
patch_r("http://localhost")  # [missing-timeout]
post_r("http://localhost")  # [missing-timeout]
put_r("http://localhost")  # [missing-timeout]
request_r("call", "http://localhost")  # [missing-timeout]

delete("http://localhost")  # [missing-timeout]
get("http://localhost")  # [missing-timeout]
head("http://localhost")  # [missing-timeout]
options("http://localhost")  # [missing-timeout]
patch("http://localhost")  # [missing-timeout]
post("http://localhost")  # [missing-timeout]
put("http://localhost")  # [missing-timeout]
request("call", "http://localhost")  # [missing-timeout]

KWARGS_WO_TIMEOUT = {}
post("http://localhost", **KWARGS_WO_TIMEOUT)  # [missing-timeout]

# requests valid cases
requests.delete("http://localhost", timeout=10)
requests.get("http://localhost", timeout=10)
requests.head("http://localhost", timeout=10)
requests.options("http://localhost", timeout=10)
requests.patch("http://localhost", timeout=10)
requests.post("http://localhost", timeout=10)
requests.put("http://localhost", timeout=10)
requests.request("call", "http://localhost", timeout=10)

delete_r("http://localhost", timeout=10)
get_r("http://localhost", timeout=10)
head_r("http://localhost", timeout=10)
options_r("http://localhost", timeout=10)
patch_r("http://localhost", timeout=10)
post_r("http://localhost", timeout=10)
put_r("http://localhost", timeout=10)
request_r("call", "http://localhost", timeout=10)

delete("http://localhost", timeout=10)
get("http://localhost", timeout=10)
head("http://localhost", timeout=10)
options("http://localhost", timeout=10)
patch("http://localhost", timeout=10)
post("http://localhost", timeout=10)
put("http://localhost", timeout=10)
request("call", "http://localhost", timeout=10)

KWARGS_TIMEOUT = {'timeout': 10}
post("http://localhost", **KWARGS_TIMEOUT)

# requests.Session methods without timeout
requests.Session().get("http://localhost")  # [missing-timeout]

session = requests.Session()
session.delete("http://localhost")  # [missing-timeout]
session.get("http://localhost")  # [missing-timeout]
session.head("http://localhost")  # [missing-timeout]
session.options("http://localhost")  # [missing-timeout]
session.patch("http://localhost")  # [missing-timeout]
session.post("http://localhost")  # [missing-timeout]
session.put("http://localhost")  # [missing-timeout]
session.request("call", "http://localhost")  # [missing-timeout]
session.post("http://localhost", **KWARGS_WO_TIMEOUT)  # [missing-timeout]

requests.Session.get(session, "http://localhost")  # [missing-timeout]

with requests.Session() as managed_session:
    managed_session.get("http://localhost")  # [missing-timeout]


# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods


class Client:
    def __init__(self):
        self.session = requests.Session()

    def fetch(self):
        return self.session.get("http://localhost")  # [missing-timeout]


class CustomSession(requests.Session):
    pass


CustomSession().get("http://localhost")  # [missing-timeout]

# requests.Session valid cases
requests.Session().get("http://localhost", timeout=10)

session.delete("http://localhost", timeout=10)
session.get("http://localhost", timeout=10)
session.head("http://localhost", timeout=10)
session.options("http://localhost", timeout=10)
session.patch("http://localhost", timeout=10)
session.post("http://localhost", timeout=10)
session.put("http://localhost", timeout=10)
session.request("call", "http://localhost", timeout=10)
session.post("http://localhost", **KWARGS_TIMEOUT)

requests.Session.get(session, "http://localhost", timeout=10)

with requests.Session() as managed_session:
    managed_session.get("http://localhost", timeout=10)

CustomSession().get("http://localhost", timeout=10)
