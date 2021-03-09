# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
class A:
    myfield: int

class B(A):
    pass

class C:
    pass

class D(C, B):
    pass


a = A()
print(a.myfield)

b = B()
print(b.myfield)

d = D()
print(d.myfield)

c = C()
print(c.myfield)  # [no-member]
