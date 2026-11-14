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

def nested_dict_value_valid():
    """assignment in an IfExp condition nested in dict values"""
    var = {
        "status": {
            "a": (
                str(var) if (var := 2) else None
            ),
        }
    }

def nested_container_value_valid():
    """recursion into nested containers: IfExp behind dict/list/call layers"""
    var = {
        "k": [x if (x := 1) else 2],
    }
    var = {
        "k": str(x if (x := 1) else 2),
    }

def complex_valid():
    """assignment within complex call expression"""
    var = str(bar(bar(a if (a:=1) else 0))).lower().upper()
    print(foo(x=foo(''.replace('', str(b if (b:=1) else 0).upper()), '', z=''), y='', z=''))

def foo(x, y, z):
    """helper function for tests"""
    return x+y+z

bar = lambda x : x


def nested_dict_unrelated_condition(flag):
    """An unrelated conditional cannot bind the enclosing assignment target."""
    value = {"before": value, "nested": {"item": 1 if flag else 0}}  # [used-before-assignment]
    return value


def nested_dict_unrelated_walrus():
    """Assigning another name cannot bind the enclosing assignment target."""
    value = {
        "before": value,  # [used-before-assignment]
        "nested": {"item": other if (other := 2) else 0},
    }
    return value


def nested_dict_deferred_lambda(flag):
    """A conditional in a deferred lambda cannot bind the outer target."""
    value = {"before": value, "deferred": lambda: 1 if flag else 0}  # [used-before-assignment]
    return value


def nested_dict_short_circuit(flag):
    """A short-circuited walrus need not bind its target before the branch."""
    value = {"nested": {"item": value if (flag or (value := 2)) else 0}}  # [used-before-assignment]
    return value


def nested_dict_read_in_test():
    """The assignment's own value is evaluated before its target is bound."""
    value = {"nested": {"item": 1 if (value := value) else 0}}  # [used-before-assignment]
    return value


def nested_dict_else_valid():
    """The condition also assigns before a direct read in its else branch."""
    value = {"nested": {"item": None if (value := None) else value}}
    return value


def nested_dict_else_call_valid():
    """A call in the else branch can use the condition's assignment."""
    value = {"nested": {"item": None if (value := None) else str(value)}}
    return value


def nested_dict_conditional_binding(flag):
    """The inner test may be skipped before a later dictionary value reads it."""
    value = {
        "nested": {
            "item": (value if (value := 2) else None) if flag else None,  # [used-before-assignment]
        },
        "after": value,
    }
    return value


def nested_dict_short_circuit_binding(flag):
    """A short circuit may skip the inner binding before a later read."""
    value = {
        "nested": {
            "item": flag and (value if (value := 2) else None),  # [used-before-assignment]
        },
        "after": value,
    }
    return value


def nested_dict_lambda_local_binding():
    """A lambda's same-name local assignment cannot initialize an outer read."""
    value = {
        "before": value,  # [used-before-assignment]
        "nested": lambda: value if (value := 2) else None,
    }
    return value
