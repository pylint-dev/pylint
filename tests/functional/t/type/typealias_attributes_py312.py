"""Test accessing TypeAliasType attributes on PEP 695 type aliases."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from typing import Literal

type MyStr = str
type MyUnion = int | str
type MyLiteral = Literal["a"]
type MyGeneric[T] = list[T]
type MyNonGenericInt[T] = int
type SimpleAlias = int

# Valid TypeAliasType attributes accesses should not emit no-member
print(MyStr.__value__)
print(MyStr.__name__)
print(MyStr.__type_params__)
print(MyStr.__parameters__)
print(MyStr.__doc__)
print(MyStr.__module__)

print(MyUnion.__value__)
print(MyUnion.__type_params__)
print(MyLiteral.__value__)

# Generic typealias subscripting and attributes
print(MyGeneric[int].__value__)
print(MyNonGenericInt[str].__value__)

# Invalid attribute accesses should still emit no-member
print(MyStr.nonexistent_attr)  # [no-member]

# Subscripting non-generic typealias should still emit unsubscriptable-object
print(SimpleAlias[int])  # [unsubscriptable-object]
