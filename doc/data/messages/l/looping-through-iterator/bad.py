# 1. Generator expressions are exhausted after one use
gen = (x for x in range(3))
for i in range(2):
    for item in gen:  # [looping-through-iterator]
        print(item)

# 2. Functional tools like map/filter/zip return one-time iterators
map_obj = map(str, range(3))
for i in range(2):
    for item in map_obj:  # [looping-through-iterator]
        print(item)

# 3. Nested producing and consuming calls containing iterator reuse will be warned
import string

iter1 = map(lambda x: x, string.printable)
iter2 = set(map(lambda x: x, string.printable))
for i in range(3):
    for i1, i2 in list(zip(iter1, iter2)):  # [looping-through-iterator]
        # iter1 is an iterator produced once and reused here.
        print(i, i1, i2)
