# pylint: disable=invalid-encoded-data, fixme
# +1: [line-too-long]
#####################################################################################################
# +1: [line-too-long]
""" that one is too long tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo loooooong"""

# The next line is exactly 80 characters long.
A = '--------------------------------------------------------------------------'

# Do not trigger the line-too-long warning if the only token that makes the
# line longer than 80 characters is a trailing pylint disable.
var = 'This line has a disable pragma and whitespace trailing beyond 80 chars. '  # pylint:disable=invalid-name

# +1: [line-too-long]
badname = 'This line is already longer than 100 characters even without the pragma. Trust me. Please.'  # pylint:disable=invalid-name

# http://example.com/this/is/a/very/long/url?but=splitting&urls=is&a=pain&so=they&can=be&long

# This a very very very ver very very long commented line with a disable directive at the end but it should not deactivate emission of messages of the same kind for lines that follow #pylint: disable=line-too-long

# +1: [line-too-long]
# This line is toooooooooooooooooooooooooooooooooooooooooooooooo looooooooooooooooooooooooooooooooooooooooong #pylint: disable=fixme

# +1: [line-too-long]
#TODO: This line is toooooooooooooooooooooooooooooooooooooooooooooooo looooooooooooooooooooooooooooooooooooooooong #pylint: disable=fixme

def function():
    # +3: [line-too-long]
    """This is a docstring.

    That contains a very, very long line that exceeds the 100 characters limit by a good margin. So good?
    """
    pass

STRING_ONE = "Just another verrrrrrrrrrrrrrrryyyyyyyyyyyyy looooooooooooooooooooooooooooooooooooooooooooooonnnnnnnnnnnnnnnnnnnnnnnnnnnnng and not so stupid line" # pylint: disable=line-too-long

# +1: [line-too-long]
STRING_TWO = "Yet another verrrrrrrrrrrrrrrryyyyyyyyyyyyy looooooooooooooooooooooooooooooooooooooooooooooonnnnnnnnnnnnnnnnnnnnnnnnnnnnng and a bit stupid line"

# pylint: disable=line-too-long
STRING_THREE = "Yet another verrrrrrrrrrrrrrrryyyyyyyyyyyyy looooooooooooooooooooooooooooooooooooooooooooooonnnnnnnnnnnnnnnnnnnnnnnnnnnnng and stupid line"


# Don't crash when the line is in a docstring
def func_with_long(parameter):
    """
    # pylint: disable=line-too-long
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccccccccccccccccccccccccc
    """
    return parameter
