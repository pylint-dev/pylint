"""test deprecated module
"""

__revision__ = 0


if __revision__:
    import Bastion 
    print Bastion
    # false positive (#10061)
    import stringfile
    print stringfile
