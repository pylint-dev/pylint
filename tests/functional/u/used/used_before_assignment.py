"""Miscellaneous used-before-assignment cases"""
# pylint: disable=consider-using-f-string, missing-function-docstring
__revision__ = None


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
    VAR5 = False
if VAR5:  # [used-before-assignment]
    pass


# Nested try
if FALSE:
    try:
        VAR6 = True
    except ValueError:
        pass
else:
    VAR6 = False
if VAR6:
    pass

if FALSE:
    try:
        VAR7 = True
    except ValueError as ve:
        print(ve)
        raise
else:
    VAR7 = False
if VAR7:
    pass

if FALSE:
    for i in range(5):
        VAR8 = i
        break
print(VAR8)

if FALSE:
    with open(__name__, encoding='utf-8') as f:
        VAR9 = __name__
print(VAR9)  # [used-before-assignment]
