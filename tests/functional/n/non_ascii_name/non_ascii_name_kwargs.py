"""
Defining non ASCII variables in a function call
"""


def okay(**kwargs):
    """Print kwargs"""
    print(kwargs)


okay(
    a_long_attribute_that_is_very_okay=1,
    b_belongs_to_yet_another_okay_attributed=2,
    łol=3,  # [non-ascii-name]
)
