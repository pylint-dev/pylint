# pylint: disable=missing-docstring,too-few-public-methods
class Entity[_T: float]:
    last_update: int | None = None

    def __init__(self, data: _T) -> None:  # [undefined-variable]  # false-positive
        self.data = data


class Sensor(Entity[int]):
    def __init__(self, data: int) -> None:
        super().__init__(data)

    def async_update(self) -> None:
        self.data = 2

        if self.last_update is None:
            pass
        self.last_update = 2


class Switch(Entity[int]):
    def __init__(self, data: int) -> None:
        Entity.__init__(self, data)


class Parent[_T]:
    def __init__(self):
        self.update_interval = 0


class Child[_T](Parent[_T]):  # [undefined-variable]  # false-positive
    def func(self):
        self.update_interval = None
