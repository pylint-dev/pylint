# pylint: disable=invalid-name,unnecessary-pass,no-else-return,useless-else-on-loop
# pylint: disable=undefined-variable,consider-using-sys-exit,unused-variable,too-many-return-statements
# pylint: disable=redefined-outer-name,using-constant-test,unused-argument,unnecessary-lambda-assignment
# pylint: disable=broad-except, not-context-manager, no-method-argument, unspecified-encoding, broad-exception-raised

"""Checks use of "too-complex" check"""


def just_a_pass():  # [too-complex]
    """McCabe rating: 1"""
    pass


def just_a_yield():  # [too-complex]
    """McCabe rating: 1"""
    yield from range(10)


def just_a_return():  # [too-complex]
    """McCabe rating: 1"""
    return 42


def just_a_raise():  # [too-complex]
    """McCabe rating: 1"""
    raise ValueError("An error occurred")


def one_edge_multiple_operations(n):  # [too-complex]
    """McCabe rating: 1"""
    k = n + 4
    s = k + n
    return s


def if_elif_else(n):  # [too-complex]
    """McCabe rating: 3"""
    if n > 3:
        return "bigger than three"
    elif n > 4:
        return "is never executed"
    else:
        return "smaller than or equal to three"


def if_with_conditionals(a, b, c):  # [too-complex]
    """McCabe rating: 2"""
    if (  # pylint: disable=too-many-boolean-expressions
        a
        and b
        or c
        or (a and not b)
        or (b and not c)
        or (c and not a)
        or (a and b and c)
    ):
        return True
    return False


def for_loop():  # [too-complex]
    """McCabe rating: 2"""
    for i in range(10):
        print(i)


def for_loop_with_else(mylist):  # [too-complex]
    """McCabe rating: 2"""
    for i in mylist:
        print(i)
    else:
        print(None)


def recursive_if_else(n):  # [too-complex]
    """McCabe rating: 2"""
    if n > 4:
        return recursive_if_else(n - 1)
    else:
        return n


def for_loop_with_break():  # [too-complex]
    """McCabe rating: 3"""
    for i in range(10):
        if i == 5:
            break


def for_loop_with_continue():  # [too-complex]
    """McCabe rating: 3"""
    for i in range(10):
        if i % 2 == 0:
            continue
        print(i)


def for_loop_with_continue_and_break():  # [too-complex]
    """McCabe rating: 4"""
    for i in range(10):
        if i % 2 == 0:
            continue
        if i % 5 == 0:
            break


def inner_functions():  # [too-complex]
    """McCabe rating: 3"""

    def inner_function():  # Known false negative ?
        """McCabe rating: 2"""

        def innermost_function():  # Known false negative ?
            """McCabe rating: 1"""
            pass

        innermost_function()

    inner_function()


def try_with_multiple_except_and_else():  # [too-complex]
    """McCabe rating: 4"""
    try:
        print(1)
    except TypeA:
        print(2)
    except TypeB:
        print(3)
    else:
        print(4)


def with_(fp):  # [too-complex]
    """McCabe rating: 1"""
    with open(fp) as f:
        content = f.read()
    return content


def lambda_with_if(lst):  # [too-complex]
    """McCabe rating should be 4, but is 1 (known false negative ?)

    See counterpart 'comprehension_with_if' below."""
    f = lambda x: [x for x in lst if x % 2 == 0] or range(10)
    return f(lst)


def comprehension_with_if(lst):  # [too-complex]
    """McCabe rating: should be 4 but is 1 (known false negative ?)
    https://github.com/PyCQA/mccabe/issues/69
    """
    return [x for x in lst if x % 2 == 0] or range(10)


def comprehension_with_if_equivalent(lst):  # [too-complex]
    """McCabe rating: 4

    See counterpart 'comprehension_with_if' above.
    """
    xs = []
    for x in lst:
        if x % 2 == 0:
            xs.append(x)
    if xs:
        return xs
    else:
        return range(10)


def nested_ifs_elifs_elses():  # [too-complex]
    """McCabe rating: 9"""
    myint = 2
    if myint > 5:
        pass
    else:
        if myint <= 5:
            pass
        else:
            myint = 3
            if myint > 2:
                if myint > 3:
                    pass
                elif myint == 3:
                    pass
                elif myint < 3:
                    pass
                else:
                    if myint:
                        pass
            else:
                if myint:
                    pass
                myint = 4


def big_elif_chain_with_nested_ifs():  # [too-complex]
    """McCabe rating: 11"""
    myint = 2
    if myint == 5:
        return myint
    elif myint == 6:
        return myint
    elif myint == 7:
        return myint
    elif myint == 8:
        return myint
    elif myint == 9:
        return myint
    elif myint == 10:
        if myint == 8:
            while True:
                return True
        elif myint == 8:
            with myint:
                return 8
    else:
        if myint == 2:
            return myint
        return myint
    return myint


class ExampleComplexityClass:
    """Class of example to test mccabe"""

    _name = "ExampleComplexityKlass"  # To force a tail.node=None

    def just_a_pass(self):  # [too-complex]
        """McCabe rating: 1"""
        pass

    def highly_complex(self, param1):  # [too-complex, too-many-branches]
        """McCabe rating: 15"""
        if not param1:
            pass
        pass
        if param1:
            pass
        else:
            pass
        pass
        if param1:
            pass
        if param1:
            pass
        if param1:
            pass
        if param1:
            pass
        if param1:
            pass
        if param1:
            pass
        if param1:
            for value in range(5):
                pass
        pass
        for count in range(6):
            with open("myfile") as fp:
                count += 1
            pass
        pass
        try:
            pass
            if not param1:
                pass
            else:
                pass
            if param1:
                raise BaseException("Error")
            with open("myfile2") as fp2:
                pass
            pass
        finally:
            if param1 is not None:
                pass
            for count2 in range(8):
                try:
                    pass
                except BaseException("Error2"):
                    pass
        return param1


for count in range(10):  # [too-complex]
    # McCabe rating: 4
    if count == 1:
        exit(0)
    elif count == 2:
        exit(1)
    else:
        exit(2)


def try_finally_with_nested_ifs():  # [too-complex]
    """McCabe rating: 3"""
    try:
        if True:
            pass
        else:
            pass
    finally:
        pass
    return True


def match_case(avg):  # [too-complex]
    """McCabe rating: 4
    See https://github.com/astral-sh/ruff/issues/11421
    """
    # pylint: disable=bare-name-capture-pattern
    match avg:
        case avg if avg < 0.3:
            avg_grade = "F"
        case avg if avg < 0.7:
            avg_grade = "E+"
        case _:
            raise ValueError(f"Unexpected average: {avg}")
    return avg_grade


def nested_match_case(data):  # [too-complex]
    """McCabe rating: 8

    Nested match statements."""
    match data:
        case {"type": "user", "data": user_data}:
            match user_data:  # Nested match adds complexity
                case {"name": str() as name}:
                    return f"User: {name}"
                case {"id": int() as user_id}:
                    return f"User ID: {user_id}"
                case _:
                    return "Unknown user format"
        case {"type": "product", "data": product_data}:
            if "price" in product_data:  # +1 for if
                return f"Product costs {product_data['price']}"
            else:
                return "Product with no price"
        case _:
            return "Unknown data type"


def yield_in_for_loop(a=None, b=None, c=None):  # [too-complex]
    """McCabe rating: 4"""
    yield from a or ()
    for elt in b:
        if elt is not None:
            yield elt
    if c is not None:
        yield c
