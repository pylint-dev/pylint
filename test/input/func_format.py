# pylint:disable=C0103,W0104,W0105
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
</body>''', 0)

assert boo <= 10, "Note is %.2f. Either you cheated, or pylint's \
broken!" % boo

def _gc_debug(gcc):
    """bad format undetected w/ py2.5"""
    ocount = {}
    for obj in gcc.get_objects():
        try:
            ocount[obj.__class__]+= 1
        except KeyError:
            ocount[obj.__class__]=1
        except AttributeError:
            pass

def hop(context):
    """multi-lines string"""
    return ['''<a id="sendbutton" href="javascript: $('%(domid)s').submit()">
<img src="%(sendimgpath)s" alt="%(send)s"/>%(send)s</a>''' % context,
            '''<a id="cancelbutton" href="javascript: history.back()">
<img src="%(cancelimgpath)s" alt="%(cancel)s"/>%(cancel)s</a>''' % context,
            ]
titreprojet = '<tr><td colspan="10">\
<img src="images/drapeau_vert.png" alt="Drapeau vert" />\
<strong>%s</strong></td></tr>' % aaaa

