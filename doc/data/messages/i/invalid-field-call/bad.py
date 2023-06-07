from dataclasses import dataclass, field


@dataclass
class C:
    a: float
    b: float
    c: float

    field(init=False)  # [invalid-field-call]

    def __post_init__(self):
        self.c = self.a + self.b


print(field(init=False))  # [invalid-field-call]
