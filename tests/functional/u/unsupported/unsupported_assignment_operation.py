"""
Checks that value used in a subscript support assignments
(i.e. defines __setitem__ method).
"""
# pylint: disable=missing-docstring,pointless-statement,expression-not-assigned,wrong-import-position,unnecessary-comprehension
# pylint: disable=too-few-public-methods,import-error,invalid-name,wrong-import-order,use-dict-literal

# primitives
numbers = [1, 2, 3]
numbers[0] = 42


bytearray(b"123")[0] = 42
dict(a=1, b=2)['a'] = 42
(1, 2, 3)[0] = 42 # [unsupported-assignment-operation]

# list/dict comprehensions are fine
[x for x in range(10)][0] = 42
{x: 10 - x for x in range(10)}[0] = 42


# instances
class NonSubscriptable:
    pass

class Subscriptable:
    def __setitem__(self, key, value):
        return key + value

NonSubscriptable()[0] = 24  # [unsupported-assignment-operation]
NonSubscriptable[0] = 24 # [unsupported-assignment-operation]
Subscriptable()[0] = 24
Subscriptable[0] = 24 # [unsupported-assignment-operation]

# generators are not subscriptable
def powers_of_two():
    k = 0
    while k < 10:
        yield 2 ** k
        k += 1

powers_of_two()[0] = 42 # [unsupported-assignment-operation]
powers_of_two[0] = 42  # [unsupported-assignment-operation]


# check that primitive non subscriptable types are caught
True[0] = 24  # [unsupported-assignment-operation]
None[0] = 42 # [unsupported-assignment-operation]
8.5[0] = 24 # [unsupported-assignment-operation]
10[0] = 24 # [unsupported-assignment-operation]

# sets are not subscriptable
{x ** 2 for x in range(10)}[0] = 24 # [unsupported-assignment-operation]
set(numbers)[0] = 24 # [unsupported-assignment-operation]
frozenset(numbers)[0] = 42 # [unsupported-assignment-operation]

# skip instances with unknown base classes
from some_missing_module import LibSubscriptable

class MaybeSubscriptable(LibSubscriptable):
    pass

MaybeSubscriptable()[0] = 42

# subscriptable classes (through metaclasses)

class MetaSubscriptable(type):
    def __setitem__(cls, key, value):
        return key + value

class SubscriptableClass(metaclass=MetaSubscriptable):
    pass

SubscriptableClass[0] = 24
SubscriptableClass()[0] = 24 # [unsupported-assignment-operation]

# functions are not subscriptable
def test(*args, **kwargs):
    return args, kwargs

test()[0] = 24 # [unsupported-assignment-operation]
test[0] = 24 # [unsupported-assignment-operation]

# deque
from collections import deque
deq = deque(maxlen=10)
deq.append(42)
deq[0] = 42

# tuples assignment
values = [1, 2, 3, 4]
(values[0], values[1]) = 3, 4
(values[0], SubscriptableClass()[0]) = 42, 42 # [unsupported-assignment-operation]

# Regression test for https://github.com/pylint-dev/pylint/issues/10050
nested_dict = {"outer": None}
nested_dict["outer"] = {"inner": None}
nested_dict["outer"]["inner"] = 42

non_subscriptable = {"outer": None}
non_subscriptable["outer"] = None
non_subscriptable["outer"]["inner"] = 42  # [unsupported-assignment-operation]


class DiscardingMapping:
    def __getitem__(self, _key):
        return None

    def __setitem__(self, _key, _value):
        pass


discarding_mapping = DiscardingMapping()
discarding_mapping["outer"] = {"inner": None}
discarding_mapping["outer"]["inner"] = 42  # [unsupported-assignment-operation]


# Shapes of https://github.com/pylint-dev/pylint/issues/10050 that the adjacent
# assignment fallback still misses: astroid keeps inferring the item from the
# container literal, so every message below is a false positive.

# An unrelated statement sits between the two assignments.
spaced_dict = {"outer": None}
spaced_dict["outer"] = {"inner": None}
print(spaced_dict)
spaced_dict["outer"]["inner"] = 42  # [unsupported-assignment-operation]  FALSE POSITIVE

# The item is read instead of written.
read_dict = {"outer": None}
read_dict["outer"] = {"inner": 42}
print(read_dict["outer"]["inner"])  # [unsubscriptable-object]  FALSE POSITIVE

# The item is deleted instead of written.
deleted_dict = {"outer": None}
deleted_dict["outer"] = {"inner": 42}
del deleted_dict["outer"]["inner"]  # [unsupported-delete-operation]  FALSE POSITIVE

# Only the outermost subscript of a chain is covered.
deep_dict = {"first": None}
deep_dict["first"] = {"second": None}
deep_dict["first"]["second"] = {"third": None}
deep_dict["first"]["second"]["third"] = 42  # [unsubscriptable-object]  FALSE POSITIVE

# The replacement is stored through an alias of the same dictionary.
aliased_dict = {"outer": None}
alias = aliased_dict
alias["outer"] = {"inner": None}
aliased_dict["outer"]["inner"] = 42  # [unsupported-assignment-operation]  FALSE POSITIVE

# The adjacent assignment stores an ambiguous value. The fallback gives up and
# the stale ``None`` from the container literal is used instead of bailing out.
def store_ambiguous(flag):
    ambiguous_dict = {"outer": None}
    ambiguous_dict["outer"] = {"inner": None} if flag else None
    ambiguous_dict["outer"]["inner"] = 42  # [unsupported-assignment-operation]  FALSE POSITIVE


# Shapes that are already handled, kept as regression guards.

def local_scope():
    local_dict = {"outer": None}
    local_dict["outer"] = {"inner": None}
    local_dict["outer"]["inner"] = 42

nested_list = [None]
nested_list[0] = {"inner": None}
nested_list[0]["inner"] = 42

augmented_dict = {"outer": None}
augmented_dict["outer"] = {"inner": 0}
augmented_dict["outer"]["inner"] += 1
