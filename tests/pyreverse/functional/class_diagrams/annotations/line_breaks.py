# OPEN BUG: https://github.com/pylint-dev/pylint/issues/8671

class A:
    p: int | None

    def f(self,
          x: (str | None) | (list[A] | list[int]),
          y: A | (int | str) | None,
    ) -> int | str | list[A | int]:
        pass
