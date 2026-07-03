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
    """False positives below this line"""
    ret = os.path.join(*parts)
    if ret:
        return ret
    print(os.path.join(*parts))
    if os.path.join(*parts):
        print()
    elif os.path.join(*parts):
        print()
    while os.path.join(*parts):
        print()
    with os.path.join(*parts): # pylint:disable=not-context-manager
        print()
    return os.path.join(*parts) + os.path.join(*parts) - os.path.join(*parts)


def kwargs_good(**kwargs):
    return func(**kwargs)


def kwargs_no_expr(**kwargs):
    ret = func(**kwargs)
    if ret:
        return ret
    print(func(**kwargs))
    if func(**kwargs):
        print()
    elif func(**kwargs):
        print()
    while func(**kwargs):
        print()
    with func(**kwargs): # pylint:disable=not-context-manager
        print()
    return func(**kwargs) + func(**kwargs) - func(**kwargs)
