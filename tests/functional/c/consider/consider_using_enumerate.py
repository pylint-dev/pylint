"""Emit a message for iteration through range and len is encountered."""

# pylint: disable=missing-docstring, import-error, unsubscriptable-object, too-few-public-methods, unnecessary-list-index-lookup, use-yield-from

def bad():
    iterable = [1, 2, 3]
    for obj in range(len(iterable)): # [consider-using-enumerate]
        yield iterable[obj]
    for obj in range(0, len(iterable)): # [consider-using-enumerate]
        yield iterable[obj]


class Bad:

    def __iter__(self):
        iterable = [1, 2, 3]
        for i in range(len(iterable)): # [consider-using-enumerate]
            yield iterable[i]

    def test(self):
        for i in range(len(self)): # [consider-using-enumerate]
            yield self[i]


def good():
    iterable = other_obj = [1, 2, 3]
    total = 0
    for obj in range(len(iterable)):
        total += obj
        yield total
        yield iterable[obj + 1: 2]
        yield iterable[len(obj)]
    for obj in iterable:
        yield iterable[obj - 1]

    for index, obj in enumerate(iterable):
        yield iterable[index]
    for index in range(0, 10):
        yield iterable[index + 1]
    for index in range(10):
        yield iterable[index]
    for index in range(len([1, 2, 3, 4])):
        yield index
    for index in range(1, len(iterable)):
        yield index
    for index in range(len(iterable)):
        yield [1, 2, 3][index]
        yield len([1, 2, 3])
    for index in range(len(iterable)):
        yield other_obj[index]

    # pylint: disable=import-outside-toplevel
    from unknown import unknown
    for index in range(unknown(iterable)):
        yield iterable[index]

    for index in range(len(iterable)):
        def test(iterable):
            return iterable[index]  # pylint: disable=cell-var-from-loop
        yield test([1, 2, 3])


class Good:

    def __iter__(self):
        # Should not suggest enumerate on self
        for i in range(len(self)):
            yield self[i]


def does_not_crash_on_range_without_args():
    for elem in range():
        print(elem)

# False negative described in #3657
# https://github.com/pylint-dev/pylint/issues/3657
class MyClass:
    def __init__(self):
        self.my_list = []

my_obj = MyClass()
def my_function(instance: MyClass):
    for i in range(len(instance.my_list)):  # [consider-using-enumerate]
        var = instance.my_list[i]
        print(var)
