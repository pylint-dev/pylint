"""Miscellaneous used-before-assignment cases"""
# pylint: disable=consider-using-f-string, missing-function-docstring


MSG = "hello %s" % MSG  # [used-before-assignment]

MSG2 = "hello %s" % MSG2  # [used-before-assignment]

def outer():
    inner()  # [used-before-assignment]
    def inner():
        pass

outer()


# pylint: disable=unused-import, wrong-import-position, import-outside-toplevel, reimported, redefined-outer-name, global-statement
import time
def redefine_time_import():
    print(time.time())  # [used-before-assignment]
    import time


def redefine_time_import_with_global():
    global time  # pylint: disable=invalid-name
    print(time.time())
    import time


# Control flow cases
FALSE = False
if FALSE:
    VAR2 = True
if VAR2:  # [used-before-assignment]
    pass

if FALSE:  # pylint: disable=simplifiable-if-statement
    VAR3 = True
elif VAR2:
    VAR3 = True
else:
    VAR3 = False
if VAR3:
    pass

if FALSE:
    VAR4 = True
elif VAR2:
    pass
else:
    VAR4 = False
if VAR4:  # [used-before-assignment]
    pass

if FALSE:
    VAR5 = True
elif VAR2:
    if FALSE:  # pylint: disable=simplifiable-if-statement
        VAR5 = True
    else:
        VAR5 = True
if VAR5:
    pass

if FALSE:
    VAR6 = False
if VAR6:  # [used-before-assignment]
    pass


# Nested try
if FALSE:
    try:
        VAR7 = True
    except ValueError:
        pass
else:
    VAR7 = False
if VAR7:
    pass

if FALSE:
    try:
        VAR8 = True
    except ValueError as ve:
        print(ve)
        raise
else:
    VAR8 = False
if VAR8:
    pass

if FALSE:
    for i in range(5):
        VAR9 = i
        break
print(VAR9)

if FALSE:
    with open(__name__, encoding='utf-8') as f:
        VAR10 = __name__
print(VAR10)  # [used-before-assignment]

for num in [0, 1]:
    VAR11 = num
    if VAR11:
        VAR12 = False
print(VAR12)

def turn_on2(**kwargs):
    """https://github.com/PyCQA/pylint/issues/7873"""
    if "brightness" in kwargs:
        brightness = kwargs["brightness"]
        var, *args = (1, "set_dimmer_state", brightness)
    else:
        var, *args = (1, "restore_dimmer_state")

    print(var, *args)
