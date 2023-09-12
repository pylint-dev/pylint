class A:
    pass


class B(A):
    pass


class C(B):  # or 'B, A' or 'A' but not 'A, B'
    pass
