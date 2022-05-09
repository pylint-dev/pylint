# pylint: disable=missing-docstring, comparison-with-itself, invalid-name


if 2 is 2:  # [literal-comparison, comparison-of-constants]
    pass

while 2 == 2:  # [comparison-of-constants]
    pass

while 2 > 2:  # [comparison-of-constants]
    pass

n = 2
if 2 != n:
    pass

if n != 1 + 1:
    pass

if True == True:  # [comparison-of-constants, singleton-comparison]
    pass

CONST = 24

if CONST is 0:  # [literal-comparison]
    pass

if CONST is 1:  # [literal-comparison]
    pass

if CONST is 42:  # [literal-comparison]
    pass

if  0 < CONST < 42:
    pass

if  0 < n < 42:
    pass

if  True == n != 42:
    pass

if  0 == n != 42:
    pass


print(0 < n < 42)
print(0 <= n < 42 )
print(n < 1 < n*42 < 42)
print(42> n <= 0)
print(0 == n > 42)
