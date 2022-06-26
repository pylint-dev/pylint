class Foo:  # [too-many-instance-attributes]
    def __init__(self):
        # max of 7 by default, can be configured
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
