"""Regression test for https://github.com/pylint-dev/pylint/issues/9410

After the None and isinstance checks, the attribute can only be the class,
which is callable.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Schema:
    pass


class Base:
    schema_class: type[Schema] | Schema | None = None

    def get_schema(self) -> Schema:
        if self.schema_class is None:
            raise NotImplementedError()
        if isinstance(self.schema_class, Schema):
            return self.schema_class
        return self.schema_class()


class WithInstance(Base):
    schema_class = Schema()


class WithClass(Base):
    schema_class = Schema
