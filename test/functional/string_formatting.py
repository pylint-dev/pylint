"""test for Python 3 string formatting error
"""
# pylint: disable=too-few-public-methods, import-error, unused-argument, star-args, line-too-long
import os
from missing import Missing

__revision__ = 1

class Custom(object):
    """ Has a __getattr__ """
    def __getattr__(self):
        return self

class Test(object):
    """ test format attribute access """
    custom = Custom()
    ids = [1, 2, 3, [4, 5, 6]]

class Getitem(object):
    """ test custom getitem for lookup access """
    def __getitem__(self, index):
        return 42

class ReturnYes(object):
    """ can't be properly infered """
    missing = Missing()

def log(message, message_type="error"):
    """ Test """
    return message

def print_good():
    """ Good format strings """
    "{0} {1}".format(1, 2)
    "{0!r:20}".format("Hello")
    "{!r:20}".format("Hello")
    "{a!r:20}".format(a="Hello")
    "{pid}".format(pid=os.getpid())
    str("{}").format(2)
    "{0.missing.length}".format(ReturnYes())
    "{1.missing.length}".format(ReturnYes())
    "{a.ids[3][1]}".format(a=Test())
    "{a[0][0]}".format(a=[[1]])
    "{[0][0]}".format({0: {0: 1}})
    "{a.test}".format(a=Custom())
    "{a.__len__}".format(a=[])
    "{a.ids.__len__}".format(a=Test())
    "{a[0]}".format(a=Getitem())
    "{a[0][0]}".format(a=[Getitem()])
    "{[0][0]}".format(["test"])
    # these are skipped
    "{0} {1}".format(*[1, 2])
    "{a} {b}".format(**{'a': 1, 'b': 2})
    "{a}".format(a=Missing())

def pprint_bad():
    """Test string format """
    "{{}}".format(1) # [too-many-format-args]
    "{} {".format() # [bad-format-string]
    "{} }".format() # [bad-format-string]
    "{0} {}".format(1, 2) # [format-combined-specification]
    # +1: [missing-format-argument-key, unused-format-string-argument]
    "{a} {b}".format(a=1, c=2)
    "{} {a}".format(1, 2) # [missing-format-argument-key]
    "{} {}".format(1) # [too-few-format-args]
    "{} {}".format(1, 2, 3) # [too-many-format-args]
    # +1: [missing-format-argument-key,missing-format-argument-key,missing-format-argument-key]
    "{a} {b} {c}".format()
    "{} {}".format(a=1, b=2) # [too-few-format-args]
    # +1: [missing-format-argument-key, missing-format-argument-key]
    "{a} {b}".format(1, 2)
    "{0} {1} {a}".format(1, 2, 3) # [missing-format-argument-key]
    # +1: [missing-format-attribute]
    "{a.ids.__len__.length}".format(a=Test())
    "{a.ids[3][400]}".format(a=Test()) # [invalid-format-index]
    "{a.ids[3]['string']}".format(a=Test()) # [invalid-format-index]
    "{[0][1]}".format(["a"]) # [invalid-format-index]
    "{[0][0]}".format(((1, ))) # [invalid-format-index]
    # +1: [missing-format-argument-key, unused-format-string-argument]
    "{b[0]}".format(a=23)
    "{a[0]}".format(a=object) # [invalid-format-index]
    log("{}".format(2, "info")) # [too-many-format-args]
    "{0.missing}".format(2) # [missing-format-attribute]
    "{0} {1} {2}".format(1, 2) # [too-few-format-args]
    "{0} {1}".format(1, 2, 3) # [too-many-format-args]
    "{0} {a}".format(a=4) # [too-few-format-args]
    "{[0]} {}".format([4]) # [too-few-format-args]
    "{[0]} {}".format([4], 5, 6) # [too-many-format-args]

def good_issue288(*args, **kwargs):
    """ Test that using kwargs does not emit a false
    positive.
    """
    'Hello John Doe {0[0]}'.format(args)
    'Hello {0[name]}'.format(kwargs)

def good_issue287():
    """ Test that the string format checker skips
    format nodes which don't have a string as a parent
    (but a subscript, name etc).
    """
    name = 'qwerty'
    ret = {'comment': ''}
    ret['comment'] = 'MySQL grant {0} is set to be revoked'
    ret['comment'] = ret['comment'].format(name)
    return ret, name

def nested_issue294():
    """ Test nested format fields. """
    '{0:>{1}}'.format(42, 24)
    '{0:{a[1]}} {a}'.format(1, a=[1, 2])
    '{:>{}}'.format(42, 24)
    '{0:>{1}}'.format(42) # [too-few-format-args]
    '{0:>{1}}'.format(42, 24, 54) # [too-many-format-args]
    '{0:{a[1]}}'.format(1) # [missing-format-argument-key]
    '{0:{a.x}}'.format(1, a=2) # [missing-format-attribute]

def issue310():
    """ Test a regression using duplicate manual position arguments. """
    '{0} {1} {0}'.format(1, 2)
    '{0} {1} {0}'.format(1) # [too-few-format-args]
