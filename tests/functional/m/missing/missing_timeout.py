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

kwargs_wo_timeout = {}
post("http://localhost", **kwargs_wo_timeout)  # [missing-timeout]

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

kwargs_timeout = {'timeout': 10}
post("http://localhost", **kwargs_timeout)
