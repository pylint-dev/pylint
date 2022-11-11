# pylint: disable=invalid-name,missing-docstring

while True:
    print("Text")

while 1:
    print("Text")

while False:
    print("Unreachable")


var = True
while var:  # [while-used]
    var = not var


def func():
    i = 0
    while i < 10:  # [while-used]
        i += 1
