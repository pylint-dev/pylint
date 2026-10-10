def module_stub_one():
    raise NotImplementedError


class Processor:

    def first(self) -> None:
        pass

    def second(self) -> None:
        pass

    def third(self) -> None:
        pass

    def fourth(self) -> None:
        pass

    def fifth(self) -> None:
        pass

    def sixth(self) -> None:
        ...

    def seventh(self) -> None:
        raise NotImplementedError

    def eighth(self) -> None:
        raise NotImplementedError(
            "must be overridden in a subclass"
        )

    def ninth(self) -> None:
        return NotImplemented

    async def tenth(self) -> None:
        pass

    def compute(self, values) -> int:
        total = 0
        for value in values:
            total += value * 2
        total *= 3
        return total

    def separator(self):
        left = 10
        right = left + 5
        return right

    def near_miss_raise_one(self):
        raise ValueError("not a placeholder")

    def near_miss_raise_two(self):
        raise ValueError("not a placeholder")

    def near_miss_raise_three(self):
        raise ValueError("not a placeholder")

    def near_miss_return_one(self):
        return None

    def near_miss_return_two(self):
        return None

    def near_miss_return_three(self):
        return None

    @abstractmethod
    def documented_stub_one(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_stub_two(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_stub_three(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_stub_four(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_stub_five(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError
