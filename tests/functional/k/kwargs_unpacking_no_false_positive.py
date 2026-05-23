"""Regression test for #8785 follow-up: ``no-value-for-parameter`` must not
fire when a required argument is supplied via ``**`` unpacking of a dict
whose full contents pylint cannot statically prove.

The patterns below were all observed as fresh false positives by the
primer run on the original #8785 fix.
"""
# pylint: disable=missing-docstring,too-few-public-methods,unused-argument


class P:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# dict.update
data_update = {"x": 1}
data_update.update({"y": 2})
P(**data_update)


# dict.setdefault
data_setdefault = {}
data_setdefault.setdefault("x", 0)
data_setdefault.setdefault("y", 0)
P(**data_setdefault)


# Loop-built dict
data_loop = {}
for key, value in [("x", 1), ("y", 2)]:
    data_loop[key] = value
P(**data_loop)


# Subscript-built dict
ATTR_X = "x"
ATTR_Y = "y"
data_subscript = {}
data_subscript[ATTR_X] = 1
data_subscript[ATTR_Y] = 2
P(**data_subscript)


# Opaque source (function return)
def get_opts():
    return {"x": 1, "y": 2}


opts = get_opts()
P(**opts)


# Forwarded **kwargs
def wrap(**kw):
    P(**kw)


wrap(x=1, y=2)
