"""Emit a message for accessing first/last element of string.split"""
# pylint: disable=line-too-long,missing-docstring,unsubscriptable-object,too-few-public-methods,invalid-name,redefined-builtin

# Test subscripting .split()
get_first = '1,2,3'.split(',')[0]  # [use-maxsplit-arg]
get_last = '1,2,3'[::-1].split(',')[0]  # [use-maxsplit-arg]

SEQ = '1,2,3'
get_first = SEQ.split(',')[0]  # [use-maxsplit-arg]
get_last = SEQ.split(',')[-1]  # [use-maxsplit-arg]
get_first = SEQ.rsplit(',')[0]  # [use-maxsplit-arg]
get_last = SEQ.rsplit(',')[-1]  # [use-maxsplit-arg]

# Don't suggest maxsplit=1 if not accessing the first or last element
get_mid = SEQ.split(',')[1]
get_mid = SEQ.split(',')[-2]


# Test varying maxsplit argument -- all these will be okay
max_split = {"maxsplit": 2}
# ## str.split() tests
good_split = '1,2,3'.split(sep=',', maxsplit=1)[-1]
good_split = '1,2,3'.split(sep=',', maxsplit=1)[0]
good_split = '1,2,3'.split(sep=',', maxsplit=2)[-1]
good_split = '1,2,3'.split(sep=',', maxsplit=2)[0]
good_split = '1,2,3'.split(sep=',', maxsplit=2)[1]
good_split = '1,2,3'.split(sep=',', **max_split)[1]

# ## str.rsplit() tests
good_split = '1,2,3'.rsplit(sep=',', maxsplit=1)[-1]
good_split = '1,2,3'.rsplit(sep=',', maxsplit=1)[0]
good_split = '1,2,3'.rsplit(sep=',', maxsplit=2)[-1]
good_split = '1,2,3'.rsplit(sep=',', maxsplit=2)[0]
good_split = '1,2,3'.rsplit(sep=',', maxsplit=2)[1]


# Tests on class attributes
class Foo():
    class_str = '1,2,3'
    def __init__(self):
        self.my_str = '1,2,3'

    def get_string(self) -> str:
        return self.my_str

# Class attributes
get_first = Foo.class_str.split(',')[0]  # [use-maxsplit-arg]
get_last = Foo.class_str.split(',')[-1]  # [use-maxsplit-arg]
get_first = Foo.class_str.rsplit(',')[0]  # [use-maxsplit-arg]
get_last = Foo.class_str.rsplit(',')[-1]  # [use-maxsplit-arg]

get_mid = Foo.class_str.split(',')[1]
get_mid = Foo.class_str.split(',')[-2]


# Test with accessors
test = Foo()
get_first = test.get_string().split(',')[0]  # [use-maxsplit-arg]
get_last = test.get_string().split(',')[-1]  # [use-maxsplit-arg]

get_mid = test.get_string().split(',')[1]
get_mid = test.get_string().split(',')[-2]


# Test with iterating over strings
list_of_strs = ["a", "b", "c", "d", "e", "f"]
for s in list_of_strs:
    print(s.split(" ")[0])  # [use-maxsplit-arg]
    print(s.split(" ")[-1])  # [use-maxsplit-arg]
    print(s.split(" ")[-2])


# Test warning messages (matching and replacing .split / .rsplit)
class Bar():
    split = '1,2,3'

# Error message should show Bar.split.split(',', maxsplit=1) or Bar.split.rsplit(',', maxsplit=1)
print(Bar.split.split(",")[0])  # [use-maxsplit-arg]
print(Bar.split.split(",")[-1])  # [use-maxsplit-arg]
print(Bar.split.rsplit(",")[0])  # [use-maxsplit-arg]
print(Bar.split.rsplit(",")[-1])  # [use-maxsplit-arg]

# Special cases
a = "1,2,3".split('\n')[0]  # [use-maxsplit-arg]
a = "1,2,3".split('split')[-1]  # [use-maxsplit-arg]
a = "1,2,3".rsplit('rsplit')[0]  # [use-maxsplit-arg]

# Test cases for false-positive reported in #4664
# https://github.com/pylint-dev/pylint/issues/4664
source = 'A.B.C.D.E.F.G'
i = 0
for j in range(5):
    print(source.split('.')[i])
    i = i + 1

sepNone = {"sep": None}
# Test for crash when sep is given by keyword
# https://github.com/pylint-dev/pylint/issues/5737
get_last = SEQ.split(sep=None)[-1]  # [use-maxsplit-arg]
get_last = SEQ.split(**sepNone)[-1]  # [use-maxsplit-arg]


class FalsePositive4857:
    def split(self, point):
        return point

obj = FalsePositive4857()
obj = obj.split((0, 0))[0]
