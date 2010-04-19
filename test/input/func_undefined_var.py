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
    augvar += 1
    del vardel

# Warning for Attribute access to undefinde attributes ?
#class Attrs(object): 
    #"""dummy class for wrong attribute access"""
#AOU = Attrs()
#AOU.number *= 1.3
#del AOU.badattr

try:
    POUET # don't catch me
except NameError:
    POUET = 'something'

try:
    POUETT # don't catch me
except Exception: # pylint:disable = W0703
    POUETT = 'something'

try:
    POUETTT # don't catch me
except: # pylint:disable = W0702
    POUETTT = 'something'

print POUET, POUETT, POUETTT


try:
    PLOUF # catch me
except ValueError:
    PLOUF = 'something'

print PLOUF

def if_branch_test(something):
    """hop"""
    if something == 0:
        if xxx == 1:
            pass
    else:
        print xxx
        xxx = 3
