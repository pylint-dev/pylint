"""https://github.com/PyCQA/pylint/issues/4265"""

try:
    f = open('test', encoding="utf-8")
except Exception:
    pass
