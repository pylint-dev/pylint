"""pylint doesn't see the NameError in this module"""

__revision__ = None

MSG = "hello %s" % MSG  # [used-before-assignment]

MSG2 = ("hello %s" %
        MSG2) # [used-before-assignment]
