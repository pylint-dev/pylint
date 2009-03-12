# pylint: disable-msg=W0104
"""snippets of codes which have at some point made pylint crash"""

__revision__ = 1

def function1(cbarg = lambda: None):
    """a strange function  """
    cbarg().x
