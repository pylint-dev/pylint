"""Test inference of values raised from function calls."""


def always_raises():
    """This function has no normal return."""
    print("aborting")
    raise ValueError("aborted")


def may_return(flag):
    """The conditional return can bypass the raise."""
    if flag:
        return
    raise ValueError("aborted")


def only_raises_conditionally(flag):
    """The function can implicitly return None."""
    if flag:
        raise ValueError("aborted")


class Aborts:  # pylint: disable=too-few-public-methods
    """Check the same inference for an ordinary bound method."""

    def abort(self):
        """This method never returns."""
        print("aborting")
        raise ValueError("aborted")


def test_raise_calls(flag):
    """Only calls that can return normally should trigger the warning."""
    if flag:
        raise always_raises()
    aborter = Aborts()
    if flag:
        raise aborter.abort()
    if flag:
        raise may_return(flag)  # [raising-bad-type]
    if flag:
        raise only_raises_conditionally(flag)  # [raising-bad-type]
    if flag:
        # pylint: disable-next=unnecessary-direct-lambda-call
        raise (lambda: None)()  # [raising-bad-type]  # noqa: PLC3002
    if flag:
        bad_value = 7
        raise bad_value  # [raising-bad-type]
    none_value = None
    raise none_value  # [raising-bad-type]
