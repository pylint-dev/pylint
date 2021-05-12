"""Emit a message for iteration through dict keys and subscripting dict with key."""
# pylint: disable=line-too-long,missing-docstring,unsubscriptable-object,too-few-public-methods,invalid-name,redefined-builtin
from collections.abc import Iterable
from typing import Any

SEQ = '1,2,3'
get_first = SEQ.split(',')[0]  # [consider-using-str-partition]
get_last = SEQ.split(',')[-1]  # [consider-using-str-partition]
get_first = SEQ.rsplit(',')[0]  # [consider-using-str-partition]
get_last = SEQ.rsplit(',')[-1]  # [consider-using-str-partition]

get_mid = SEQ.split(',')[1]  # This is okay
get_mid = SEQ.split(',')[-2]  # This is okay

# Test with storing splits as an object
split1 = SEQ.split(',')
get_first = split1[0]  # [consider-using-str-partition]
get_last = split1[-1]  # [consider-using-str-partition]
get_last = split1[len(split1)-1]  # [consider-using-str-partition]

split2 = SEQ.rsplit(',')
get_first = split2[0]  # [consider-using-str-partition]
get_last = split2[-1]  # [consider-using-str-partition]
get_last = split2[len(split2)-1]  # [consider-using-str-partition]

print(split1[0], split1[-1])  # [consider-using-str-partition, consider-using-str-partition]

# Test when running len on another iterable
some_list = []
get_last = split1[len(split2)-1]  # Should not throw an error

# Tests on class attributes
class Foo():
    class_str = '1,2,3'

    def __init__(self):
        self.my_str = '1,2,3'

    def get_string(self) -> str:
        return self.my_str

# Class attributes
get_first = Foo.class_str.split(',')[0]  # [consider-using-str-partition]
get_last = Foo.class_str.split(',')[-1]  # [consider-using-str-partition]
get_first = Foo.class_str.rsplit(',')[0]  # [consider-using-str-partition]
get_last = Foo.class_str.rsplit(',')[-1]  # [consider-using-str-partition]

get_mid = Foo.class_str.split(',')[1]
get_mid = Foo.class_str.split(',')[-2]

split2 = Foo.class_str.split(',')
get_first = split2[0]  # [consider-using-str-partition]
get_last = split2[-1]  # [consider-using-str-partition]
get_last = split2[len(split2)-1]  # [consider-using-str-partition]

# Test with accessors
bar = Foo()
get_first = bar.get_string().split(',')[0]  # [consider-using-str-partition]
get_last = bar.get_string().split(',')[-1]  # [consider-using-str-partition]

get_mid = bar.get_string().split(',')[1]
get_mid = bar.get_string().split(',')[-2]

# Test with iterating over strings
list_of_strs = ["a", "b", "c", "d", "e", "f"]
for s in list_of_strs:
    print(s.split(" ")[0])  # [consider-using-str-partition]
    print(s.split(" ")[-1])  # [consider-using-str-partition]
    print(s.split(" ")[-2])

# Test with user-defined len function
def len(x: Iterable[Any]) -> str:
    return f"Hello, world! {x[2]}"

get_last = split2[len(split2)-1]  # This won't throw the warning as the len function has been redefined
