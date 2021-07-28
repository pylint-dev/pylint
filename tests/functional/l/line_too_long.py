# pylint: disable=fixme, unnecessary-pass
# +1: [line-too-long]
#####################################################################################################
# +1: [line-too-long]
""" that one is too long tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo loooooong"""

# The next line is exactly 80 characters long.
A = "--------------------------------------------------------------------------"

# Do not trigger the line-too-long warning if the only token that makes the
# line longer than 80 characters is a trailing pylint disable.
# pylint:disable=invalid-name
var = (
    "This line has a disable pragma and whitespace trailing beyond 80 chars. "
)

# +1: [line-too-long]
badname = "This line is already longer than 100 characters even without the pragma. Trust me. Please."  # pylint:disable=invalid-name

# http://example.com/this/is/a/very/long/url?but=splitting&urls=is&a=pain&so=they&can=be&long


# +1: [line-too-long]
# This line is toooooooooooooooooooooooooooooooooooooooooooooooo looooooooooooooooooooooooooooooooooooooooong #pylint: disable=fixme

# +1: [line-too-long]
# TODO: This line is toooooooooooooooooooooooooooooooooooooooooooooooo looooooooooooooooooooooooooooooooooooooooong #pylint: disable=fixme


def function():
    # +3: [line-too-long]
    """This is a docstring.

    That contains a very, very long line that exceeds the 100 characters limit by a good margin. So good?
    """
    pass


# Don't crash when the line is in a docstring
def func_with_long(parameter):
    """
    # pylint: disable=line-too-long
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccccccccccccccccccccccccc
    """
    return parameter


# No line-too-long message should be emitted as the disable comment stands for all the multiline
def issue_2957():
    """
    This is a very very very long line within a docstring that should trigger a pylint C0301 error line-too-long

    Even spread on multiple lines, the disable command is still effective on very very very, maybe too much long docstring
    """#pylint: disable=line-too-long
    return True


def issue_2957_bis():
    # +3: [line-too-long]
    # +4: [line-too-long]
    """
    This is a very very very long line within a docstring that should trigger a pylint C0301 error line-too-long

    Even spread on multiple lines, the disable command is still effective on very very very, maybe too much long docstring
    """
    return True


# +2: [line-too-long]
# +2: [line-too-long]
VAR = """A very very long, maybe too much, constant. Just here to trigger message emission and check everything is fine and nice"""
"""But it is however too long, isn't it? I don't know what to say more here. I got a lack of imagination, just listening to music..."""


# +1: [line-too-long]
VAR_BIS = """A very very long, maybe too much, constant. Just here to trigger message emission and check everything is fine and nice"""
"""But it is however too long, isn't it? I don't know what to say more here. I got a lack of imagination, just listening to music..."""#pylint: disable=line-too-long
