# pylint: disable=missing-docstring,bare-except,pointless-statement,superfluous-parens, consider-using-f-string
def strangeproblem():
    try:
        for _ in range(0, 4):
            message = object()
            print(type(message))
    finally:
        message = object()


try:
    my_int = 1
    print("MY_INT = %d" % my_int)
finally:
    my_int = 2

try:
    pass
except:
    false_positive = 1
    false_positive  # here pylint claims used-before-assignment
finally:
    false_positive = 2  # this line is needed to reproduce the issue
