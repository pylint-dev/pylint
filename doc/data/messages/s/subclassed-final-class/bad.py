from typing import final


@final
class Base:
    ...


class MyClass(Base):  # [subclassed-final-class]
    ...
