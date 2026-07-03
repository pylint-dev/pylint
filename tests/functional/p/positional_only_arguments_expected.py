# pylint: disable=missing-docstring,unused-argument,pointless-statement
# pylint: disable=too-few-public-methods, kwarg-superseded-by-positional-arg

class Gateaux:
    def nihon(self, a, r, i, /, cheese=False):
        return f"{a}{r}{i}gateaux" + " au fromage" if cheese else ""


CAKE = Gateaux()
# Should not emit error
CAKE.nihon(1, 2, 3)
CAKE.nihon(1, 2, 3, True)
CAKE.nihon(1, 2, 3, cheese=True)
# Emits error
CAKE.nihon(1, 2, i=3)  # [positional-only-arguments-expected]
CAKE.nihon(1, r=2, i=3)  # [positional-only-arguments-expected]
CAKE.nihon(a=1, r=2, i=3)  # [positional-only-arguments-expected]
CAKE.nihon(1, r=2, i=3, cheese=True)  # [positional-only-arguments-expected]


def function_with_kwargs(apple, banana="Yellow banana", /, **kwargs):
    """
    Calling this function with the `banana` keyword should not emit
    `positional-only-arguments-expected` since it is added to `**kwargs`.

    >>> function_with_kwargs("Red apple", banana="Green banana")
    >>> "Red apple"
    >>> "Yellow banana"
    >>> {"banana": "Green banana"}
    """
    print(apple)
    print(banana)
    print(kwargs)


function_with_kwargs("Red apple", banana="Green banana")
