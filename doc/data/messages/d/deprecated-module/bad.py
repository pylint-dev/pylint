from copy import deepcopy # [deprecated-module]

#Create an empty tuple
x = ()
print(x)
#Create an empty tuple with tuple() function built-in Python
Tuple1 = tuple()
print(Tuple1)

Tuple8 = ("HELLO", 5, [], True)
print(Tuple8)
#make a copy of a tuple using deepcopy() function
Tuple8_colon = deepcopy(Tuple8)
Tuple8_colon[2].append(50)
print(Tuple8_colon)
print(Tuple8)