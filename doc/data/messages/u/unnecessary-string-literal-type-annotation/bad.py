class Foo:
    def some_function(self) -> "Bar":  # [unnecessary-string-literal-type-annotation]
        ...


class Bar:
    def another_function(self) -> "Foo":  # [unnecessary-string-literal-type-annotation]
        ...
