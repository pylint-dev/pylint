from dataclasses import dataclass, field, make_dataclass

C = make_dataclass(
    "C",
    [("x", int), "y", ("z", int, field(default=5))],
    namespace={"add_one": lambda self: self.x + 1},
)


@dataclass
class C:
    a: float
    b: float
    c: float = field(init=False)

    def __post_init__(self):
        self.c = self.a + self.b
