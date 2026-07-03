"""used-before-assignment (E0601)"""
def function():
    """Consider that except blocks may not execute."""
    try:
        pass
    except ValueError:
        some_message = 'some message'

    if not some_message:  # [used-before-assignment]
        return 1

    return some_message


def uses_nonlocal():
    """https://github.com/pylint-dev/pylint/issues/5965"""
    count = 0
    def inner():
        nonlocal count
        try:
            print(count)
        except ValueError:
            count +=1

    return inner()


def uses_unrelated_nonlocal():
    """Unrelated nonlocals still let messages emit"""
    count = 0
    unrelated = 0
    def inner():
        nonlocal unrelated
        try:
            print(count)  # [used-before-assignment]
        except ValueError:
            count += 1

    print(count)
    return inner()


# Cases related to a specific control flow where
# the `else` of a loop can depend on a name only defined
# in a single except handler because that except handler is the
# only non-break exit branch.

def valid_only_non_break_exit_from_loop_is_except_handler():
    """https://github.com/pylint-dev/pylint/issues/5683"""
    for _ in range(3):
        try:
            function()  # not an exit branch because of `else` below
        except ValueError as verr:
            error = verr  # < exit branch where error is defined
        else:
            break  # < exit condition where error is *not* defined
            # will skip else: raise error
        print("retrying...")
    else:
        # This usage is valid because there is only one exit branch
        raise error


def invalid_no_outer_else():
    """The reliance on the name is not guarded by else."""
    for _ in range(3):
        try:
            function()
        except ValueError as verr:
            error = verr
        else:
            break
        print("retrying...")
    raise error  # [used-before-assignment]


def invalid_no_outer_else_2():
    """Same, but the raise is inside a loop."""
    for _ in range(3):
        try:
            function()
        except ValueError as verr:
            error = verr
        else:
            break
        raise error  # [used-before-assignment]


def invalid_no_inner_else():
    """No inner else statement."""
    for _ in range(3):
        try:
            function()
        except ValueError as verr:
            error = verr
        print("retrying...")
        if function():
            break
    else:
        raise error  # [used-before-assignment]


def invalid_wrong_break_location():
    """The break is in the wrong location."""
    for _ in range(3):
        try:
            function()
            break
        except ValueError as verr:
            error = verr
            print("I give up")
    else:
        raise error  # [used-before-assignment]


def invalid_no_break():
    """No break."""
    for _ in range(3):
        try:
            function()
        except ValueError as verr:
            error = verr
        else:
            pass
    else:  # pylint: disable=useless-else-on-loop
        raise error  # [used-before-assignment]


def invalid_other_non_break_exit_from_loop_besides_except_handler():
    """The continue creates another exit branch."""
    while function():
        if function():
            continue
        try:
            pass
        except ValueError as verr:
            error = verr
        else:
            break
    else:
        raise error  # [used-before-assignment]


def valid_continue_does_not_matter():
    """This continue doesn't matter: still just one exit branch."""
    while function():
        try:
            for _ in range(3):
                if function():
                    continue
                print(1 / 0)
        except ZeroDivisionError as zde:
            error = zde
        else:
            break
    else:
        raise error


def invalid_conditional_continue_after_break():
    """The continue is another exit branch"""
    while function():
        try:
            if function():
                break
            if not function():
                continue
        except ValueError as verr:
            error = verr
        else:
            break
    else:
        raise error  # [used-before-assignment]


def invalid_unrelated_loops():
    """The loop else in question is not related to the try/except/else."""
    for _ in range(3):
        try:
            function()
        except ValueError as verr:
            error = verr
        else:
            break
    while function():
        print('The time is:')
        break
    else:
        raise error  # [used-before-assignment]


def valid_nested_loops():
    """The name `error` is still available in a nested else."""
    for _ in range(3):
        try:
            function()
        except ValueError as verr:
            error = verr
        else:
            break
    else:
        while function():
            print('The time is:')
            break
        else:
            raise error
