# pylint: disable=missing-docstring, invalid-name

MY_DICTIONARY = {"key_one": 1, "key_two": 2, "key_three": 3}

try:  # [too-many-try-statements]
    value = MY_DICTIONARY["key_one"]
    value += 1
    print("This one has an except clause only.")
except KeyError:
    pass

try:  # [too-many-try-statements]
    value = MY_DICTIONARY["key_one"]
    value += 1
    print("This one has a finally clause only.")
finally:
    pass

try:  # [too-many-try-statements]
    value = MY_DICTIONARY["key_one"]
    value += 1
    print("This one has an except clause...")
    print("and also a finally clause!")
except KeyError:
    pass
finally:
    pass

try:  # [too-many-try-statements]
    if "key_one" in MY_DICTIONARY:
        entered_if_body = True
        print("This verifies that content inside of an if statement is counted too.")
    else:
        entered_if_body = False

    while False:
        print("This verifies that content inside of a while loop is counted too.")

    for item in []:
        print("This verifies that content inside of a for loop is counted too.")


except KeyError:
    pass

try:
    value = MY_DICTIONARY["key_one"]
except KeyError:
    value = 0

# A sole pass is required to keep these suites syntactically valid (#9418).
try:
    with open("blah.txt", "a", encoding="ascii"):
        pass
except OSError:
    pass

try:
    if "key_one" in MY_DICTIONARY:
        pass
except KeyError:
    pass

try:
    for item in MY_DICTIONARY:
        pass
except KeyError:
    pass

try:
    while MY_DICTIONARY:
        pass
except KeyError:
    pass

# The with statement itself and subsequent work must still count.
try:  # [too-many-try-statements]
    with open("blah.txt", "a", encoding="ascii"):
        pass
    value = 1
except OSError:
    pass

# A pass alongside another statement is not a required placeholder.
try:  # [too-many-try-statements]
    value = 1
    pass  # [unnecessary-pass]
except KeyError:
    pass
