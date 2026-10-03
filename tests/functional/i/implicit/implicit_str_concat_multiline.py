#pylint: disable=missing-docstring

TEST_TUPLE = ('a', 'b'  # [implicit-str-concat]
              'c')

# See https://github.com/pylint-dev/pylint/issues/8552.
PARENTHESIZED_IS_OK = [
    "a",
    (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
        " sed do eiusmod tempor incididunt ut labore et dolore "
    ),
]

# Single argument without trailing comma is OK:
print(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
    " sed do eiusmod tempor incididunt ut labore et dolore "
    "magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea "
)

# Implicit concatenated strings on the same line always raises:
print(
    "Lorem ipsum dolor sit amet, ""consectetur adipiscing elit,"  # [implicit-str-concat]
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
    " sed do eiusmod tempor incididunt ut labore et dolore "
    "magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea "
)

# Explicitly wrapping in parens with a trailing comma is OK:
print(
    (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
        " sed do eiusmod tempor incididunt ut labore et dolore "
        "magna aliqua. Ut enim ad minim veniam, quis nostrud "
        "exercitation ullamco laboris nisi ut aliquip ex ea "
    ),
)

# But NOT OK when there is a trailing comma and NOT wrapped in parens:
print(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit," # [implicit-str-concat]
    " sed do eiusmod tempor incididunt ut labore et dolore "
    "magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea ",
)
