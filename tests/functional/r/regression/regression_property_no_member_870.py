# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
# https://github.com/pylint-dev/pylint/issues/870

class X:
    def __init__(self, val=None):
        self._val = val
    @property
    def val(self):
        return self._val
    @val.setter
    def val(self, value):
        self._val = value

if __name__ == '__main__':
    print(X([]).val.append)
