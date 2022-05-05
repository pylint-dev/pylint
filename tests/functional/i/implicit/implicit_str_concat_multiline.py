#pylint: disable=missing-docstring

TEST_TUPLE = ('a', 'b'  # [implicit-str-concat]
              'c')

print(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit," # [implicit-str-concat]
    " sed do eiusmod tempor incididunt ut labore et dolore "
    "magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea "
)
