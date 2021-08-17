# pylint: disable=missing-docstring, invalid-name, line-too-long, multiple-statements, pointless-string-statement, pointless-statement
var = "string"
var_two = "extra string"

x = f"This is a {var} which should be a f-string"
x = "This is a {var} used twice, see {var}"
x = "This is a {var} which should be a f-string"  # [possible-forgotten-f-prefix]
x = "This is a {var} and {var_two} which should be a f-string"  # [possible-forgotten-f-prefix, possible-forgotten-f-prefix]
x1, x2, x3 = (1, 2, "This is a {var} which should be a f-string")  # [possible-forgotten-f-prefix]

y = "This is a {var} used for formatting later"  # [possible-forgotten-f-prefix]
z = y.format(var="string")

g = "This is a {another_var} used for formatting later"  # [possible-forgotten-f-prefix]
h = g.format(another_var="string")

i = "This is {invalid /// python /// inside}"
j = "This is {not */ valid python.}"
k = "This is {def function(): return 42} valid python but not an expression"

def function(): return 42

examples = [var, var_two]
x = f"This is an example with a list: {''.join(examples) + 'well...' }"
x = "This is an example with a list: {''.join(examples) + 'well...' }"  # [possible-forgotten-f-prefix]

param = "string"
"This is a string" # good
"This is a {param}" # [possible-forgotten-f-prefix]
f"This is a {param}" # good

"This is a calculation: 1 + 1" # good
"This is a calculation: {1 + 1}" # [possible-forgotten-f-prefix]
f"This is a calculation: {1 + 1}" # good

"This is a nice string" # good
"This is a {'nice' + param}" # [possible-forgotten-f-prefix]
f"This is a {'nice' + param}" # good
