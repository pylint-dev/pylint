class P:
    def __init__(self, name: str):
        self.name = name


class PrivateAttr:
    def __init__(self):
        self.__x = P("private")


class ProtectedAttr:
    def __init__(self):
        self._x = P("protected")


class PublicAttr:
    def __init__(self):
        self.x = P("public")


class SpecialAttr:
    def __init__(self):
        self.__x__ = P("special")
