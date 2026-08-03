def can_form_triangle(a, b, c):
    # The two checks contradict each other: if ``a`` is strictly greater
    # than ``b``, then ``b`` cannot also be strictly greater than ``a``.
    return a > b and b > a and c > 0  # [impossible-comparison]
