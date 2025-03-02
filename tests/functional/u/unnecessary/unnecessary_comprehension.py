# pylint: disable=undefined-variable, pointless-statement, missing-docstring, line-too-long, expression-not-assigned
# For name-reference see https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries

# List comprehensions
[x for x in iterable]  # [unnecessary-comprehension]
[y for x in iterable]  # expression != target_list
[x for x in iterable] # [unnecessary-comprehension] use list(iterable)
[x for x,y,z in iterable]  # expression != target_list
[(x, y) for x, y in iterable]  # [unnecessary-comprehension]
[(x,y,z) for x,y,z in iterable]  # [unnecessary-comprehension]
[(x,y,z) for (x,y,z) in iterable]  # [unnecessary-comprehension]
[x for x, *y in iterable]  # expression != target_list
[x for x in iterable if condition]  # exclude comp_if
[y for x in iterable for y in x]  # exclude nested comprehensions
[2 * x for x in iterable]  # exclude useful comprehensions
[(x, y, 1) for x, y in iterable]  # exclude useful comprehensions
# Test case for issue #4499
a_dict = {}
b_dict = [(k, v) for k, v in a_dict.items()]  # [unnecessary-comprehension]

# Set comprehensions
{x for x in iterable}  # [unnecessary-comprehension]
{y for x in iterable}  # expression != target_list
{x for x,y,z in iterable}  # expression != target_list
{(x,y,z) for x,y,z in iterable}  # [unnecessary-comprehension]
b_dict = {(x,y,z) for (x, y, z) in iterable}  # [unnecessary-comprehension]
{(x,y,z) for x in iterable}  # expression != target_list
{(x,y,(a,b,c)) for x in iterable}  # expression != target_list
{x for x, *y in iterable}  # expression != target_list
{x for x in iterable if condition}  # exclude comp_if
{y for x in iterable for y in x}  # exclude nested comprehensions

# Dictionary comprehensions
{x: y for x, y in iterable}  # [unnecessary-comprehension]
{y: x for x, y in iterable}  # key value wrong order
{x: y for (x, y) in iterable}  # [unnecessary-comprehension]
{x: y for x,y,z in iterable}  # expression != target_list
{x: y for x, y in iterable if condition}  # exclude comp_if
{y: z for x in iterable for y, z in x}  # exclude nested comprehensions
{x: 1 for x in iterable}  # expression != target_list
{2 * x: 3 + x for x in iterable}  # exclude useful comprehensions

# Some additional tests on helptext -- when object is already a list/set/dict
my_list = []
my_dict = {}
my_set = set()

[elem for elem in my_list]  # [unnecessary-comprehension]
ITEMS = {k: v for k, v in my_dict.items()} # [unnecessary-comprehension]
{k: my_dict[k] for k in my_dict} # [consider-using-dict-items]
{elem for elem in my_set}  # [unnecessary-comprehension]
