# pylint: disable=missing-docstring,invalid-name,undefined-variable,too-few-public-methods

a1 = 2
if a1:  # [consider-using-assignment-expr]
    ...

# Do not suggest assignment expressions if assignment spans multiple lines
a2 = (
    1,
)
if a2:
    ...

# Only first name should be replaced
a3 = 2
if a3 == a3_a:  # [consider-using-assignment-expr]
    ...

# Above black line length
a4 = some_loooooooonnnnnngggg_object_name.with_some_really_long_function_name(arg)
if a4:
    ...

def func_a():
    a5 = some___object.function_name_is_just_long_enough_to_fit_in_line()  # some comment
    if a5 is None:  # [consider-using-assignment-expr]
        ...

    # Using assignment expression would result in line being 89 chars long
    a6 = some_long_object.function_name_is_too_long_enough_to_fit___line()
    if a6 is None:
        ...

# Previous unrelate note should not match
print("")
if a7:
    ...


b1: int = 2
if b1:  # [consider-using-assignment-expr]
    ...

b2 = some_function(2, 3)
if b2:  # [consider-using-assignment-expr]
    ...

b3 = some_object.variable
if b3:  # [consider-using-assignment-expr]
    ...


# UnaryOp
c1 = 2
if not c1:  # [consider-using-assignment-expr]
    ...


# Compare
d1 = 2
if d1 is True:  # [consider-using-assignment-expr]
    ...

d2 = 2
if d2 is not None:  # [consider-using-assignment-expr]
    ...

d3 = 2
if d3 == 2:  # [consider-using-assignment-expr]
    ...


# -----
# Don't emit warning if match statement would be a better fit
o1 = 2
if o1 == 1:
    ...
elif o1 == 2:
    ...
elif o1 == 3:
    ...

o2 = 2
if o2 == 1:
    ...
elif o2:
    ...

o3 = 2
if o3 == 1:  # [consider-using-assignment-expr]
    ...
else:
    ...

o4 = 2
if o4 == 1:  # [consider-using-assignment-expr]
    ...
elif o4 and o4_other:
    ...

o5 = 2
if o5 == 1:  # [consider-using-assignment-expr]
    ...
elif o5_other == 1:
    ...

o6 = 2
if o6 == 1:  # [consider-using-assignment-expr]
    ...
elif o6_other:
    ...

def func_p():
    p1 = 2
    if p1 == 1:
        return
    if p1 == 2:
        return

    p2 = 2
    if p2 == 1:
        return
    if p2:
        return

    p3 = 2
    if p3 == 1:  # [consider-using-assignment-expr]
        ...
    else:
        ...

    p4 = 2
    if p4 == 1:  # [consider-using-assignment-expr]
        ...
    elif p4 and p4_other:
        ...

    p5 = 2
    if p5 == 1:  # [consider-using-assignment-expr]
        ...
    elif p5_other == 1:
        ...

    p6 = 2
    if p6 == 1:  # [consider-using-assignment-expr]
        ...
    elif p6_other:
        ...


# -----
# Assignment expression does NOT work for attribute access
# Make sure not to emit message!
class A:
    var = 1

A.var = 2
if A.var:
    ...
