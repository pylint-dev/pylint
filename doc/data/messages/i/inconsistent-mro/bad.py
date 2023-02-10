class A:
    pass


class B(A):
    pass


class C(A, B):  # [inconsistent-mro]
    pass
