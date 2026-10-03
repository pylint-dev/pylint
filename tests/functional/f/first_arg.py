# pylint: disable=missing-docstring
"""check for methods first arguments
"""


class Obj:
    # C0202, classmethod
    def __new__(something):  # [bad-classmethod-argument]
        pass

    # C0202, classmethod
    def class1(cls):
        pass
    class1 = classmethod(class1)  # [no-classmethod-decorator]

    def class2(other):  # [bad-classmethod-argument]
        pass
    class2 = classmethod(class2)  # [no-classmethod-decorator]


class Meta(type):
    # C0204, metaclass __new__
    def __new__(other, name, bases, dct):  # [bad-mcs-classmethod-argument]
        pass

    # C0203, metaclass method
    def method1(cls):
        pass

    def method2(other):  # [bad-mcs-method-argument]
        pass

    # C0205, metaclass classmethod
    def class1(mcs):
        pass
    class1 = classmethod(class1)  # [no-classmethod-decorator]

    def class2(other):  # [bad-mcs-classmethod-argument]
        pass
    class2 = classmethod(class2)  # [no-classmethod-decorator]
