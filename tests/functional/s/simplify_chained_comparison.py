"""Test that some boolean expression statement tests can be simplified."""

# pylint: disable=missing-docstring, invalid-name, no-else-return, too-many-branches


def test_simplify_chained_comparison_1():
    a = 1
    b = 2
    c = 3
    return a < b and b < c # [chained-comparison]


def test_simplify_chained_comparison_2():
    a = 1
    return a < 10 and a > 1 # [chained-comparison]


def test_simplify_chained_comparison_3():
    a = 1
    b = 2
    c = 3
    d = 4
    if a < 10 and a > 1: # [chained-comparison]
        pass
    elif a > 1 and a < 10: # [chained-comparison]
        pass
    elif a > 1 and a <= 10: # [chained-comparison]
        pass
    elif a > 1 and a == 10: # [chained-comparison]
        pass
    elif a > 1 and a > 10: # [chained-comparison]
        pass
    elif a < 100 and a < 10: # [chained-comparison]
        pass
    elif a < b and a == 1 and a < c: # [chained-comparison]
        pass
    elif a > 1 and a < 10 and b == 2: # [chained-comparison]
        pass
    elif a > 1 and c == b and a < 10: # [chained-comparison]
        pass
    elif a < b and b < c: # [chained-comparison]
        pass
    elif a > b and b > c: # [chained-comparison]
        pass
    elif a < b and a == 1 and b < c: # [chained-comparison]
        pass
    elif a < b and b < c and c == 786: # [chained-comparison]
        pass
    elif a < b and b < 0 and c == 786: # [chained-comparison]
        pass
    elif a < b and c == 786 and b < 0: # [chained-comparison]
        pass
    elif c == 786 and b < 0 and a < b: # [chained-comparison]
        pass
    elif a < b < c and c < d: # [chained-comparison]
        pass
    elif b < c < d and a < b: # [chained-comparison]
        pass
    elif a < b < c and a < b and b < c: # [chained-comparison]
        pass
    elif a < b < c and a < c: # [chained-comparison]
        pass
    elif 0.5 < a and a < 1.5: # [chained-comparison]
        pass


def test_not_simplify_chained_comparison_1():
    a = 1
    b = 2
    c = 3
    d = 4
    if a < 10 and b > 1:
        pass
    elif a > 1 and b < 10:
        pass
    elif a == 1 and b == 2:
        pass
    elif a == 1 and a == 2:
        pass
    elif a == b and b == c:
        pass
    elif a < b and a < c:
        pass
    elif a < b and a < c and c == 786:
        pass
    elif a < b < c and b < d:
        pass
    elif a < b < c and a < d:
        pass
    elif b < c < d and a < c:
        pass
    elif b < c < d and a < d:
        pass


def test_impossible_comparison():
    a = 1
    b = 2
    c = 3
    d = 4
    if a > b and b > a: # [impossible-comparison]
        pass
    elif a > 100 and a < b and b < 15: # [impossible-comparison]
        pass
    elif a > b and b > c and c > a: # [impossible-comparison]
        pass
    elif a > b and b > c and c > d and d >= a: # [impossible-comparison]
        pass
    elif a > 100 and c == b and a < 10: # [impossible-comparison]
        pass
    elif a > b and b == a: # [impossible-comparison]
        pass
    elif a >= b and b > a: # [impossible-comparison]
        pass
    elif a < 5 and a > 5: # [impossible-comparison]
        pass


def test_all_equal():
    a = 1
    b = 2
    c = 3
    d = 4
    if a >= b and b >= a: # [chained-comparison-all-equal]
        pass
    elif a >= b and b >= c and c >= a: # [chained-comparison-all-equal]
        pass
    elif a <= b and b <= c and c <= d and d <= a: # [chained-comparison-all-equal]
        pass
    # A cycle that runs through a literal is still a cycle of weak
    # inequalities: this one only says ``a == 5``.
    elif a >= 5 and 5 >= a: # [chained-comparison-all-equal]
        pass
    elif a >= 5 and 5 >= b and b >= a: # [chained-comparison-all-equal]
        pass


def test_chained_comparison_with_unprocessable_operands():
    """Non-comparison operands should be preserved verbatim in the suggestion."""
    def is_int(value):
        return isinstance(value, int)

    v = int(input())
    if is_int(v) and v >= 0 and v <= 999: # [chained-comparison]
        pass
    if v >= 0 and v <= 999 and v != 42: # [chained-comparison]
        pass
    # The type guard must stay before the numeric range even when it appears
    # between two comparisons in the source: pulling it across the chain
    # would change short-circuit evaluation.
    if v >= 0 and is_int(v) and v <= 999:
        pass
    items = (1, 2, 3)
    if items[0] < 5 and v > 1 and v < 10: # [chained-comparison]
        pass
    if 5 > items[0] and v > 1 and v < 10: # [chained-comparison]
        pass


def test_cycles_do_not_cross_unprocessable_boundaries():
    """Known limit: an unprocessable statement breaks cycle detection.

    A boundary statement (``is_int(v)``, ``v != 42``, ...) can short-circuit
    before later comparisons are evaluated, so a cycle that only closes when
    we cross such a boundary is *not* unconditionally impossible. The checker
    deliberately bails out rather than risk a false positive.
    """
    def is_int(value):
        return isinstance(value, int)

    a = int(input())
    b = int(input())
    v = int(input())
    # Pre-boundary check: when the cycle lives entirely inside a run of
    # consecutive comparisons we still report it.
    if a > b and b > a and is_int(v):  # [impossible-comparison]
        pass
    if a >= b and b >= a and is_int(v):  # [chained-comparison-all-equal]
        pass
    # Cross-boundary cycle: the guard sits between the two halves, so the
    # checker keeps quiet even though ``a > b and b > a`` is a contradiction.
    if a > b and is_int(v) and b > a:
        pass
    if a >= b and is_int(v) and b >= a:
        pass


def test_boundary_keeps_its_parentheses():
    """A boundary looser than ``and`` must stay parenthesized.

    The suggestion joins its parts with ``and``, so dropping the parentheses
    around ``b or c`` would suggest a different expression.
    """
    a = int(input())
    b, c, d = 1, 2, 3
    if a > 1 and a < 10 and (b or c): # [chained-comparison]
        pass
    if a > 1 and a < 10 and (b if c else d): # [chained-comparison]
        pass
    if a > 1 and a < 10 and (b := c): # [chained-comparison]
        pass


def test_several_cycles():
    a, b, c, d = 1, 2, 3, 4
    # Two contradictions, but the condition can only be False once.
    if a > b and b > a and c > d and d > c: # [impossible-comparison]
        pass
    # Two independent groups of equal operands, each worth its own message.
    # +1: [chained-comparison-all-equal,chained-comparison-all-equal]
    if a >= b and b >= a and c >= d and d >= c:
        pass
    # A single contradiction is enough to silence the equality groups.
    if a > b and b > a and c >= d and d >= c: # [impossible-comparison]
        pass


def test_comparison_with_itself_is_a_boundary():
    """``comparison-with-itself`` owns these, so no chain is suggested."""
    a, b = 1, 2
    if a >= a and b > 0: # [comparison-with-itself]
        pass
    if a > a and b > 0: # [comparison-with-itself]
        pass
    if a > b and b >= b: # [comparison-with-itself]
        pass


def test_a_literal_equality_does_not_link_two_conditions():
    """``fruit == 0`` is a fact about ``fruit``, not a link in a chain."""
    apples, bananas, cherries = 1, 2, 3
    # Chaining these through the ``0`` would suggest ``bananas < 0 == apples``,
    # which reads worse than the two conditions it replaces.
    if apples == 0 and bananas < 0:
        pass
    # Two inequalities may still meet on a literal.
    if apples < 0 and bananas >= 0: # [chained-comparison]
        pass
    # ``786`` has nothing to do with the rest, so it gains no ``786 > 0`` edge.
    if apples < bananas and bananas < 0 and cherries == 786: # [chained-comparison]
        pass


def test_suggestion_is_truncated():
    """A part we can't fold in is spliced in verbatim, so this can grow."""
    def looks_like_a_ripe_banana(fruit):
        return fruit > 0

    def smells_like_a_ripe_banana(fruit):
        return fruit > 0

    banana = int(input())
    # +1: [chained-comparison]
    if (looks_like_a_ripe_banana(banana) and smells_like_a_ripe_banana(banana)
            and banana > 1 and banana < 10):
        pass


def test_negative_literals():
    """``-1`` is a minus applied to ``1``, but it is still a number."""
    apples = int(input())
    if apples > -1 and apples < 5: # [chained-comparison]
        pass
    if apples > -1 and apples > 3: # [chained-comparison]
        pass
    if apples < -5 and apples > -1: # [impossible-comparison]
        pass
    if -1.5 < apples and apples < -0.5: # [chained-comparison]
        pass
