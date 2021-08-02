# pylint: disable=missing-module-docstring, invalid-name
var = "string"
var_two = "extra string"

x = f"This is a {var} which should be a f-string"
x = "This is a {var} used twice, see {var}"
x = "This is a {var} which should be a f-string"  # [possible-f-string-as-string]
x = "This is a {var} and {var_two} which should be a f-string"  # [possible-f-string-as-string]
x1, x2, x3 = (1, 2, "This is a {var} which should be a f-string")  # [possible-f-string-as-string]

y = "This is a {var} used for formatting later"
z = y.format(var="string")
