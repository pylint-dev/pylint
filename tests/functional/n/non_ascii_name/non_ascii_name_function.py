"""invalid ASCII char in a function definition"""
# pylint: disable=invalid-name


def sayHello():
    """Greetings"""
    print("Hello, World!")


# +3: [non-ascii-name]


def sayНello():
    """From Russia with Love"""
    print("Goodbye, World!")


# Usage should not raise a second error
sayНello()
