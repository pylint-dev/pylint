"""Emit a message for iteration through dict keys and subscripting dict with key."""
# pylint: disable=line-too-long,missing-docstring,unsubscriptable-object,too-few-public-methods,invalid-name,redefined-builtin


# Test varying maxsplit argument
bad_split = '1,2,3'.split(sep=',',maxsplit=1)  # [consider-using-str-partition]
bad_split = '1,2,3'[::-1].split(',',1)  # [consider-using-str-partition]

good_split = '1,2,3'[::-1].split(',',2)
good_split = '1,2,3'[::-1].split(',')

good_split = '1,2,3'[::-1].split(',',2)[0]  #This is fine, we ignore cases where maxsplit > 1
good_split = '1,2,3'[::-1].split(',',2)[-1]  #This is fine, we ignore cases where maxsplit > 1


# Test subscripting .split()
get_first = '1,2,3'.split(',')[0]  # [consider-using-str-partition]
get_last = '1,2,3'[::-1].split(',')[0]  # [consider-using-str-partition]

SEQ = '1,2,3'
get_first = SEQ.split(',')[0]  # [consider-using-str-partition]
get_last = SEQ.split(',')[-1]  # [consider-using-str-partition]
get_first = SEQ.rsplit(',')[0]  # [consider-using-str-partition]
get_last = SEQ.rsplit(',')[-1]  # [consider-using-str-partition]

get_mid = SEQ.split(',')[1]  # This is okay
get_mid = SEQ.split(',')[-2]  # This is okay


# Test with storing splits as an object
split1 = SEQ.split(',')  # [consider-using-str-partition]
get_first = split1[0]
get_last = split1[-1]

split2 = SEQ.rsplit(',')  # [consider-using-str-partition]
get_first = split2[0]
get_last = split2[-1]

split3 = SEQ.rsplit(',')  # This is fine, split3 indexed with [1]
get_first = split3[0]
get_middle = split3[1]
get_last = split3[-1]

split1, split2 = SEQ.split(','), SEQ.rsplit(',')  # [consider-using-str-partition, consider-using-str-partition]
get_first = split1[0]
get_last = split1[-1]
get_first = split2[0]
get_last = split2[-1]

split1, split2 = SEQ.split(','), SEQ.rsplit(',')  # This is fine, both splits are utilized
get_first = split1[0]
get_last = split1[-1]
get_first = split2[0]
get_last = split2[-1]
split1[1] = split2[1]


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

split2 = Foo.class_str.split(',')  # [consider-using-str-partition]
get_first = split2[0]
get_last = split2[-1]


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


# Test warning messages (matching and replacing .split / .rsplit)
class Bar():
    split = '1,2,3'

print(Bar.split.split(",")[0])  # [consider-using-str-partition] (Error message should show Bar.split.partition)
print(Bar.split.split(",")[-1])  # [consider-using-str-partition] (Error message should show Bar.split.rpartition)
print(Bar.split.rsplit(",")[0])  # [consider-using-str-partition] (Error message should show Bar.split.partition)
print(Bar.split.rsplit(",")[-1])  # [consider-using-str-partition] (Error message should show Bar.split.rpartition)
