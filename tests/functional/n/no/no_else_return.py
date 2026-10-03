""" Test that superfluous else return are detected. """


# pylint:disable=invalid-name,missing-docstring,unused-variable
def foo1(x, y, z):
    if x:  # [no-else-return]
        a = 1
        return y
    else:
        b = 2
        return z


def foo2(x, y, w, z):
    if x:  # [no-else-return]
        a = 1
        return y
    elif z:
        b = 2
        return w
    else:
        c = 3
        return z


def foo3(x, y, z):
    if x:
        a = 1
        if y:  # [no-else-return]
            b = 2
            return y
        else:
            c = 3
            return x
    else:
        d = 4
        return z


def foo4(x, y):
    if x:   # [no-else-return]
        if y:
            a = 4
        else:
            b = 2
        return
    else:
        c = 3
    return


def foo5(x, y, z):
    if x:   # [no-else-return]
        if y:
            a = 4
        else:
            b = 2
        return
    elif z:
        c = 2
    else:
        c = 3
    return


def foo6(x, y):
    if x:
        if y:   # [no-else-return]
            a = 4
            return
        else:
            b = 2
    else:
        c = 3
    return


def bar1(x, y, z):
    if x:
        return y
    return z


def bar2(w, x, y, z):
    if x:
        return y
    if z:
        a = 1
    else:
        return w
    return None


def bar3(x, y, z):
    if x:
        if z:
            return y
    else:
        return z
    return None


def bar4(x):
    if x:  # [no-else-return]
        return True
    else:
        try:
            return False
        except ValueError:
            return None

# pylint: disable = bare-except
def try_one_except() -> bool:
    try:  # [no-else-return]
        print('asdf')
    except:
        print("bad")
        return False
    else:
        return True


def try_multiple_except() -> bool:
    try:  # [no-else-return]
        print('asdf')
    except TypeError:
        print("bad")
        return False
    except ValueError:
        print("bad second")
        return False
    else:
        return True

def try_not_all_except_return() -> bool:  # [inconsistent-return-statements]
    try:
        print('asdf')
    except TypeError:
        print("bad")
        return False
    except ValueError:
        val = "something"
    else:
        return True

# pylint: disable = raise-missing-from
def try_except_raises() -> bool:
    try:  # [no-else-raise]
        print('asdf')
    except:
        raise ValueError
    else:
        return True

def try_except_raises2() -> bool:
    try:  # [no-else-raise]
        print('asdf')
    except TypeError:
        raise ValueError
    except ValueError:
        raise TypeError
    else:
        return True

def test() -> bool:  # [inconsistent-return-statements]
    try:
        print('asdf')
    except RuntimeError:
        return False
    finally:
        print("in finally")


def try_finally_return() -> bool:  # [inconsistent-return-statements]
    try:
        print('asdf')
    except RuntimeError:
        return False
    else:
        print("inside else")
    finally:
        print("in finally")

def try_finally_raise():
    current_tags = {}
    try:
        yield current_tags
    except Exception:
        current_tags["result"] = "failure"
        raise
    else:
        current_tags["result"] = "success"
    finally:
        print("inside finally")
