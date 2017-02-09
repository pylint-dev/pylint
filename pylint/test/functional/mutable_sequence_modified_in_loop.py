# coding: utf-8
""" The mutable sequence was modified inside the loop """

# pylint:disable=print-statement, missing-docstring, redefined-outer-name, invalid-name, using-constant-test, no-member


class MyList(object):

    def __init__(self):
        self.my_list = range(1, 6)

    def __iter__(self):
        return iter(self.my_list)

    def remove(self, item):
        pass

    def delete(self, item):
        pass

    def pop(self, item):
        pass


my_list = MyList()
for item in my_list:
    my_list.remove(item)

my_list = MyList()
for item in my_list:
    my_list.delete(item)

my_list = MyList()
for item in my_list:
    my_list.pop(item)


items = range(1, 6)
for item in items:
    items.remove(item)  # [mutable-sequence-modified-in-loop]

items = list([1, 2, 3, 4, 5, 6])
for item in items:
    items.pop(item)  # [mutable-sequence-modified-in-loop]

items = range(1, 6)
for item in list(items):
    items.remove(item)

items = range(1, 6)
for item in items:
    items.remove(item)  # [mutable-sequence-modified-in-loop]

items = range(1, 6)
for item in items:
    if True:
        items.remove(item)  # [mutable-sequence-modified-in-loop]
        if True:
            items.pop()  # [mutable-sequence-modified-in-loop]

my_list = [1, 2, 3]
my_seq = my_list
for i in my_seq:
    my_list.pop()
    my_seq.append(4)  # [mutable-sequence-modified-in-loop]
    my_seq.extend([5, 6, 7])  # [mutable-sequence-modified-in-loop]
