# pylint: disable=too-few-public-methods,import-error, no-absolute-import,missing-docstring, misplaced-comparison-constant
# pylint: disable=useless-super-delegation,wrong-import-position,invalid-name, wrong-import-order

if len('TEST'):  # [len-as-condition]
    pass

if not len('TEST'):  # [len-as-condition]
    pass

z = False
if z and len(['T', 'E', 'S', 'T']):  # [len-as-condition]
    pass

if True or len('TEST'):  # [len-as-condition]
    pass

if len('TEST') == 0:  # Should be fine
    pass

if len('TEST') < 1:  # Should be fine
    pass

if len('TEST') <= 0:  # Should be fine
    pass

if 1 > len('TEST'):  # Should be fine
    pass

if 0 >= len('TEST'):  # Should be fine
    pass

if z and len('TEST') == 0:  # Should be fine
    pass

if 0 == len('TEST') < 10:  # Should be fine
    pass

if 0 < 1 <= len('TEST') < 10:  # Should be fine
    pass

if 10 > len('TEST') != 0:  # Should be fine
    pass

if 10 > len('TEST') > 1 > 0:  # Should be fine
    pass

if 0 <= len('TEST') < 100:  # Should be fine
    pass

if z or 10 > len('TEST') != 0:  # Should be fine
    pass

if z:
    pass
elif len('TEST'):  # [len-as-condition]
    pass

if z:
    pass
elif not len('TEST'):  # [len-as-condition]
    pass

while len('TEST'):  # [len-as-condition]
    pass

while not len('TEST'):  # [len-as-condition]
    pass

while z and len('TEST'):  # [len-as-condition]
    pass

while not len('TEST') and z:  # [len-as-condition]
    pass

assert len('TEST') > 0  # Should be fine

x = 1 if len('TEST') != 0 else 2  # Should be fine

f_o_o = len('TEST') or 42  # Should be fine

a = x and len(x)  # Should be fine

def some_func():
    return len('TEST') > 0  # Should be fine

def github_issue_1325():
    l = [1, 2, 3]
    length = len(l) if l else 0  # Should be fine
    return length

def github_issue_1331(*args):
    assert False, len(args)  # Should be fine

def github_issue_1331_v2(*args):
    assert len(args), args  # [len-as-condition]

def github_issue_1331_v3(*args):
    assert len(args) or z, args  # [len-as-condition]

def github_issue_1331_v4(*args):
    assert z and len(args), args  # [len-as-condition]
