"""
non ascii variable defined in a function
"""


def okay(
    just_some_thing_long_again: str,
    lol_very_long_argument: str,
    łol: str,  # [non-ascii-name]
) -> bool:
    """Be okay, yeah?"""
    # Usage should not raise a second error
    print(just_some_thing_long_again, lol_very_long_argument, łol)
    return True


# Usage should raise a second error
okay(
    "A          VVVVVVVEEEERRRRRRRRRRYYYYYYYYYY    LONG TIME               ",
    lol_very_long_argument="a",
    łol="b",  # [non-ascii-name]
)
