# pylint: disable=W0640
"""Check a nested function defined in a loop."""

def example(args):
    """The check"""
    for i in args:
        def nested():
            print(i)
        nested()
    for i in args:
        print(i)
