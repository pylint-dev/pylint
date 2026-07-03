"""Tests for used-before-assignment false positive from ternary expression with walrus operator"""
# pylint: disable=unnecessary-lambda-assignment, unused-variable, disallowed-name, invalid-name

def invalid():
    """invalid cases that will trigger used-before-assignment"""
    var = foo(a, '', '')  # [used-before-assignment]
    print(str(1 if (a:=-1) else 0))
    var = bar(b)  # [used-before-assignment]
    var = c*c  # [used-before-assignment]
    var = 1 if (b:=-1) else 0
    var = 1 if (c:=-1) else 0

def attribute_call_valid():
    """assignment with attribute calls"""
    var = (a if (a:='a') else '').lower()
    var = ('' if (b:='b') else b).lower()
    var = (c if (c:='c') else c).upper().lower().replace('', '').strip()
    var = ''.strip().replace('', '' + (e if (e:='e') else '').lower())

def function_call_arg_valid():
    """assignment as function call arguments"""
    var = str(a if (a:='a') else '')
    var = str('' if (b:='b') else b)
    var = foo(1, c if (c:=1) else 0, 1)
    print(foo('', '', foo('', str(int(d if (d:='1') else '')), '')))

def function_call_keyword_valid():
    """assignment as function call keywords"""
    var = foo(x=a if (a:='1') else '', y='', z='')
    var = foo(x='', y=foo(x='', y='', z=b if (b:='1') else ''), z='')

def dictionary_items_valid():
    """assignment as dictionary keys/values"""
    var = {
        0: w if (w:=input()) else "",
    }
    var = {
        x if (x:=input()) else "": 0,
    }
    var = {
        0: y if (y:=input()) else "",
        z if (z:=input()) else "": 0,
    }

def complex_valid():
    """assignment within complex call expression"""
    var = str(bar(bar(a if (a:=1) else 0))).lower().upper()
    print(foo(x=foo(''.replace('', str(b if (b:=1) else 0).upper()), '', z=''), y='', z=''))

def foo(x, y, z):
    """helper function for tests"""
    return x+y+z

bar = lambda x : x
