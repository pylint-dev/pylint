"""test deprecated module
"""

__revision__ = 0


if __revision__:
    import optparse
    print optparse
    # false positive (#10061)
    import stringfile
    print stringfile
