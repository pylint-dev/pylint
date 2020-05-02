# pylint: disable=undefined-variable, pointless-statement, missing-docstring, line-too-long
# For name-reference see https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries

# List comprehensions
[x for x in iterable]  # [unnecessary-comprehension]
[y for x in iterable]  # expression != target_list
[x for x,y,z in iterable]  # expression != target_list
[(x,y,z) for x,y,z in iterable]  # [unnecessary-comprehension]
[(x,y,z) for (x,y,z) in iterable]  # [unnecessary-comprehension]
[x for x, *y in iterable]  # expression != target_list
[x for x in iterable if condition]  # exclude comp_if
[y for x in iterable for y in x]  # exclude nested comprehensions
[2 * x for x in iterable]  # exclude useful comprehensions
[(x, y, 1) for x, y in iterable]  # exclude useful comprehensions

# Set comprehensions
{x for x in iterable}  # [unnecessary-comprehension]
{y for x in iterable}  # expression != target_list
{x for x,y,z in iterable}  # expression != target_list
{(x,y,z) for x,y,z in iterable}  # [unnecessary-comprehension]
{(x,y,z) for (x, y, z) in iterable}  # [unnecessary-comprehension]
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
