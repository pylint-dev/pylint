"""Test that unused-import is not emitted here when everything else is disabled

https://github.com/PyCQA/pylint/issues/3445
"""
from os import environ

for k, v in environ.items():
    print(k, v)
