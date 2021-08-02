# pylint: disable=missing-module-docstring, invalid-name, line-too-long
var = "string"
var_two = "extra string"

x = f"This is a {var} which should be a f-string"
x = "This is a {var} used twice, see {var}"
x = "This is a {var} which should be a f-string"  # [possible-forgotten-f-prefix]
x = "This is a {var} and {var_two} which should be a f-string"  # [possible-forgotten-f-prefix, possible-forgotten-f-prefix]
x1, x2, x3 = (1, 2, "This is a {var} which should be a f-string")  # [possible-forgotten-f-prefix]

y = "This is a {var} used for formatting later"
z = y.format(var="string")

examples = [var, var_two]
x = f"This is an example with a list: {''.join(examples) + 'well...' }"
x = "This is an example with a list: {''.join(examples) + 'well...' }"  # [possible-forgotten-f-prefix]
