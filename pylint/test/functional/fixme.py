# -*- encoding=utf-8 -*-
# pylint: disable=missing-docstring, unused-variable

# +1: [fixme]
# FIXME: beep


def function():
    variable = "FIXME: Ignore me!"
    # +1: [fixme]
    test = "text"  # FIXME: Valid test

    # +1: [fixme]
    # TODO: Do something with the variables
    # +1: [fixme]
    xxx = "n/a"  # XXX: Fix this later
    # +1: [fixme]
    #FIXME: no space after hash
    #FIXME: in fact nothing to fix #pylint: disable=fixme
    #TODO: in fact nothing to do #pylint: disable=fixme
    #TODO: in fact nothing to do #pylint: disable=line-too-long, fixme
