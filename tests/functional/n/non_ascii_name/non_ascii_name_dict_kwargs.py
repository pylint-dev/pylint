"""
We don't expect this to give any errors!
"""


def okay(**kwargs):
    """print kwargs"""
    print(kwargs)


KEYWORD_ARGS = {"łol": "this would be hard to check against"}

okay(**KEYWORD_ARGS)
