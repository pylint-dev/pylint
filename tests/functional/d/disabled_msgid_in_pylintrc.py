"""https://github.com/PyCQA/pylint/issues/4265"""

try:
    f = open('test')
except Exception:
    pass
