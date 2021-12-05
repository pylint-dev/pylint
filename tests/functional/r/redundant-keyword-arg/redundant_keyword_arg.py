# pylint: disable=missing-docstring, too-few-public-methods,useless-object-inheritance, consider-using-f-string


def function_default_arg(one=1, two=2):
    """function with default value"""
    return two, one


function_default_arg(1, one=5)  # [redundant-keyword-arg]

# Don't emit a redundant-keyword-arg for this example,
# it's perfectly valid


class Issue642(object):
    attr = 0

    def __str__(self):
        return "{self.attr}".format(self=self)
