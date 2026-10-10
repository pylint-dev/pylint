# pylint: disable=missing-docstring, use-list-literal, use-dict-literal, line-too-long, unnecessary-lambda-assignment, unnecessary-lambda
import collections

HEHE = {}

def function1(value=[]): # [dangerous-default-value]
    """docstring"""
    return value

def function2(value=HEHE): # [dangerous-default-value]
    """docstring"""
    return value

def function3(value):
    """docstring"""
    return value

def function4(value=set()): # [dangerous-default-value]
    """set is mutable and dangerous."""
    return value

def function5(value=frozenset()):
    """frozenset is immutable and safe."""
    return value

GLOBAL_SET = set()

def function6(value=GLOBAL_SET): # [dangerous-default-value]
    """set is mutable and dangerous."""
    return value

def function7(value=dict()): # [dangerous-default-value]
    """dict is mutable and dangerous."""
    return value

def function8(value=list()):  # [dangerous-default-value]
    """list is mutable and dangerous."""
    return value

def function9(value=[1, 2, 3, 4]): # [dangerous-default-value]
    """list with items should not output item values in error message"""
    return value

def function10(value={'a': 1, 'b': 2}): # [dangerous-default-value]
    """dictionaries with items should not output item values in error message"""
    return value

def function11(value=list([1, 2, 3])): # [dangerous-default-value]
    """list with items should not output item values in error message"""
    return value

def function12(value=dict([('a', 1), ('b', 2)])): # [dangerous-default-value]
    """dictionaries with items should not output item values in error message"""
    return value

OINK = {
    'a': 1,
    'b': 2
}

def function13(value=OINK): # [dangerous-default-value]
    """dictionaries with items should not output item values in error message"""
    return value

def function14(value=dict([(1, 2), (1, 2, 3)])): # [dangerous-default-value]
    """a dictionary which will not be inferred to a syntax AST, but to an
    astroid.Instance.
    """
    return value

INVALID_DICT = dict([(1, 2), (1, 2, 3)])

def function15(value=INVALID_DICT): # [dangerous-default-value]
    """The same situation as function14."""
    return value

def function16(value={1}): # [dangerous-default-value]
    """set literal as default value"""
    return value

def function17(value=collections.deque()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function18(value=collections.ChainMap()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function19(value=collections.Counter()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function20(value=collections.OrderedDict()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function21(value=collections.defaultdict()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function22(value=collections.UserDict()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function23(value=collections.UserList()):  # [dangerous-default-value]
    """mutable, dangerous"""
    return value

def function24(*, value=[]): # [dangerous-default-value]
    """dangerous default value in kwarg."""
    return value


class Clazz:
    # pylint: disable=too-few-public-methods
    def __init__(  # [dangerous-default-value]
        self,
        arg: str = None,
        *,
        kk: dict = {},
    ) -> None:
        pass


def default_key() -> str:
    return f"{collections.OrderedDict()}.json"


def call_in_default(key=default_key()):  # [dangerous-default-value]
    return key


def call_in_kwonly(*, key=default_key()):  # [dangerous-default-value]
    return key


def call_attribute(name="a".upper()):  # [dangerous-default-value]
    return name


def call_nested(values=(default_key(),)):  # [dangerous-default-value]
    return values


def call_in_expression(value=1 + len("abc")):  # [dangerous-default-value]
    return value


def two_calls(a=default_key(), b=default_key()):  # [dangerous-default-value, dangerous-default-value]
    return a, b


async def call_async(key=default_key()):  # [dangerous-default-value]
    return key


class WithCall:
    # pylint: disable=too-few-public-methods
    def method(self, key=default_key()):  # [dangerous-default-value]
        return key


def mutable_call_reported_once(value=list()):  # [dangerous-default-value]
    return value


def immutable_calls(a=tuple(), b=frozenset(), c=int("1"), d=str(), e=object()):
    return a, b, c, d, e


def callable_defaults(factory=default_key, callback=lambda: default_key()):
    return factory, callback


class FrozenStore(frozenset):
    pass


def subclass_of_immutable(store=FrozenStore()):
    return store
