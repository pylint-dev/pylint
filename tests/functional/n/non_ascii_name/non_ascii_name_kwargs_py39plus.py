"""
Defining non ASCII variables in a function call

This test is 3.9+ and not using 'min_pyver_end_position'
as the starting column is also incorrect on < 3.9
"""


def okay(**kwargs):
    """Print kwargs"""
    print(kwargs)


okay(
    a_long_attribute_that_is_very_okay=1,
    b_belongs_to_yet_another_okay_attributed=2,
    łol=3,  # [non-ascii-name]
)
