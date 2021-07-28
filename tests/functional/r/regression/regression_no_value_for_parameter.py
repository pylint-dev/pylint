# pylint: disable=missing-docstring,import-error
import os

from Unknown import Unknown


class ConfigManager(Unknown):


    RENAMED_SECTIONS = {
        'permissions': 'content'
    }

    def test(self):
        self.RENAMED_SECTIONS.items() #@

    def items(self, sectname, raw=True):
        pass


def func(*, key=None):
    return key


def varargs_good(*parts):
    """All good"""
    return os.path.join(*parts)


def varargs_no_expr(*parts):
    """False positive below this line"""
    ret = os.path.join(*parts)
    return ret


def kwargs_good(**kwargs):
    return func(**kwargs)


def kwargs_no_expr(**kwargs):
    ret = func(**kwargs)
    return ret
