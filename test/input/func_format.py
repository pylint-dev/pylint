# pylint:disable-msg=C0103,W0104,W0105
"""Check format
"""
__revision__ = ''

notpreceded= 1
notfollowed =1
notfollowed <=1

correct = 1
correct >= 1

def func(arg, arg2):
    """test named argument
    """
    func(arg=arg+1,
         arg2=arg2-arg)

aaaa,bbbb = 1,2
aaaa |= bbbb
aaaa &= bbbb


if aaaa: pass
else:
    aaaa,bbbb = 1,2
    aaaa,bbbb = bbbb,aaaa

bbbb = (1,2,3)

aaaa = bbbb[1:]
aaaa = bbbb[:1]
aaaa = bbbb[:]

aaaa = {aaaa:bbbb}


# allclose(x,y) uses |x-y|<ATOL+RTOL*|y|
"""docstring,should not match
isn't it:yes!
a=b
"""
aaaa = 'multiple lines\
string,hehehe'


boo = 2 # allclose(x,y) uses |x-y|<ATOL+RTOL*|y|

def other(funky):
    """yo, test formatted result with indentation"""
    funky= funky+2
    
html = """<option value="=">ist genau gleich</option>
yo+=4
"""
html2 = """<option value='='>ist genau gleich</option>
yo+=4
"""

func('''<body>Hello
</body>''')

assert boo <= 10, "Note is %.2f. Either you cheated, or pylint's \
broken!" % boo
