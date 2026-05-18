def can_form_triangle(a, b, c):
    # Triangle inequality: each side must be shorter than the sum of the
    # other two.
    return a + b > c and b + c > a and a + c > b
