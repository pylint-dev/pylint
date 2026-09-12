def module_stub_two():
    raise NotImplementedError


class AnotherProcessor:

    def alpha(self) -> None:
        pass

    def beta(self) -> None:
        pass

    def gamma(self) -> None:
        pass

    def delta(self) -> None:
        pass

    def epsilon(self) -> None:
        pass

    def zeta(self) -> None:
        ...

    def eta(self) -> None:
        raise NotImplementedError

    def theta(self) -> None:
        raise NotImplementedError(
            "must be overridden in a subclass"
        )

    def iota(self) -> None:
        return NotImplemented

    async def kappa(self) -> None:
        pass

    def calculate(self, values) -> int:
        total = 0
        for value in values:
            total += value * 2
        total *= 3
        return total

    def divider(self):
        top = 99
        bottom = top - 9
        return bottom

    def other_raise_one(self):
        raise ValueError("not a placeholder")

    def other_raise_two(self):
        raise ValueError("not a placeholder")

    def other_raise_three(self):
        raise ValueError("not a placeholder")

    def other_return_one(self):
        return None

    def other_return_two(self):
        return None

    def other_return_three(self):
        return None

    @abstractmethod
    def documented_other_one(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_other_two(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_other_three(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_other_four(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def documented_other_five(self) -> None:
        """To be implemented by subclasses."""
        raise NotImplementedError
