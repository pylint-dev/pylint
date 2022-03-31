from typing import final


class Base:
    @final
    def my_method(self):
        pass


class Subclass(Base):
    def my_other_method(self):
        pass
