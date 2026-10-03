"""Test unnecessary direct calls to lambda expressions."""
# pylint: disable=undefined-variable, line-too-long

y = (lambda x: x**2 + 2*x + 1)(a)  # [unnecessary-direct-lambda-call]
y = max((lambda x: x**2)(a), (lambda x: x+1)(a))  # [unnecessary-direct-lambda-call,unnecessary-direct-lambda-call]


class ClassBodyWalrus:  # pylint: disable=too-few-public-methods
    """The lambda supplies the scope PEP 572 requires.

    An assignment expression inside a comprehension is a SyntaxError when the
    containing scope is a class body, so inlining these would not compile.
    """

    generator = (lambda: all((x := object()) is x for _ in range(1)))()
    listcomp = (lambda: [(x := o) for o in range(1)])()
    setcomp = (lambda: {(x := o) for o in range(1)})()
    dictcomp = (lambda: {(x := o): o for o in range(1)})()

    # Still reported: no comprehension, so the walrus is legal in a class body.
    bare_walrus = (lambda: (x := 1))()  # [unnecessary-direct-lambda-call]
    # Still reported: no assignment expression in the comprehension.
    plain_comprehension = (lambda: [o + 1 for o in range(1)])()  # [unnecessary-direct-lambda-call]
    # Still reported for both calls: after inlining the outer lambda, the
    # comprehension is still inside the inner one, which keeps its own scope.
    nested = (lambda: [(lambda: [(x := o) for o in range(1)])()])()  # [unnecessary-direct-lambda-call,unnecessary-direct-lambda-call]


def outside_a_class_body():
    """Only a class body carries the restriction."""
    return (lambda: all((x := object()) is x for _ in range(1)))()  # [unnecessary-direct-lambda-call]
