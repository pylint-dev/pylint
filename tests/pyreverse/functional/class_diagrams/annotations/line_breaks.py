# OPEN BUG: https://github.com/pylint-dev/pylint/issues/8671

class A:
    def f(self, x: str | None):
        pass
