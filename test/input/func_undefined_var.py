"""test access to undefined variables"""

__revision__ = '$Id:'

DEFINED = 1

if DEFINED != 1:
    if DEFINED in (unknown, DEFINED):
        DEFINED += 1


def in_method(var):
    """method doc"""
    var = nomoreknown
    assert var

DEFINED = {DEFINED:__revision__}
DEFINED[__revision__] = OTHER = 'move this is astng test'

OTHER += '$'

def bad_default(var, default=unknown2):
    """function with defaut arg's value set to an unexistant name"""
    print var, default
    print xxxx
    print xxxx #see story #1000
