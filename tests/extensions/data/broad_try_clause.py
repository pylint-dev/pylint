# pylint: disable=missing-docstring, invalid-name

MY_DICTIONARY = {"key_one": 1, "key_two": 2, "key_three": 3}

try:  # [max-try-statements]
    value = MY_DICTIONARY["key_one"]
    value += 1
    print("This one has an except clause only.")
except KeyError:
    pass

try:  # [max-try-statements]
    value = MY_DICTIONARY["key_one"]
    value += 1
    print("This one has an finally clause only.")
finally:
    pass

try:  # [max-try-statements]
    value = MY_DICTIONARY["key_one"]
    value += 1
    print("This one has an except clause...")
    print("and also a finally clause!")
except KeyError:
    pass
finally:
    pass

try:  # [max-try-statements]
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
