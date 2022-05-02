"""
We don't expect this to give any errors!
"""


def okay(**kwargs):
    """print kwargs"""
    print(kwargs)


keyword_args = {"łol": "this would be hard to check against"}

okay(**keyword_args)
