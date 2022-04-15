class Foo:
    def __init__(self, param):
        if self.param:  # [access-member-before-definition]
            pass
        self.param = param
