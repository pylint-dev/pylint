"""https://github.com/pylint-dev/pylint/issues/4265"""

try:
    F = open('test', encoding="utf-8")
except Exception:
    pass
