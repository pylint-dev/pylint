"""test a warning is triggered when using for a lists comprehension variable"""
from __future__ import print_function
__revision__ = 'yo'

TEST_LC = [C for C in __revision__ if C.isalpha()]
print(C) # WARN
C = 4
print(C) # this one shouldn't trigger any warning

B = [B for B in  __revision__ if B.isalpha()]
print(B) # nor this one

for var1, var2 in TEST_LC:
    var1 = var2 + 4
print(var1) # WARN

for note in __revision__:
    note.something()
for line in __revision__:
    for note in line:
        A = note.anotherthing()


for x in []:
    pass
for x in range(3):
    print((lambda: x)()) # OK
