from typing import TypeVar, Iterable, Tuple, NewType

MyTypeVar = TypeVar('MyTypeVar', int, float, complex)
Vector = Iterable[Tuple[MyTypeVar, MyTypeVar]]
AnyStr = TypeVar('AnyStr', str, bytes)
UserId = NewType('UserId', str)

my_type_var = TypeVar('my_type_var', int, float, complex)  # [invalid-name]
vector = Iterable[Tuple[my_type_var, my_type_var]]  # [invalid-name]
any_str = TypeVar('any_str', str, bytes)  # [invalid-name]
user_id = NewType('user_id', str)  # [invalid-name]
