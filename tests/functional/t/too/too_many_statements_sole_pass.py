# A sole ``pass`` (or the stub-style sole ``...``) only makes an empty body
# syntactically valid; it is not an author-written statement, so it must not
# add to the too-many-statements count. The historical count for every other
# body shape is what tests/functional/t/too/too_many_statements.py checks.
# pylint: disable=missing-docstring, invalid-name, unnecessary-pass


def empty_with_sole_pass():
    pass


async def empty_async_with_sole_pass():
    pass


def empty_with_sole_ellipsis(): ...


async def empty_async_with_sole_ellipsis(): ...


# Controls: keep the historical count for every other body shape (both sides
# of the new branch, including the short-circuit where the body has one node
# that is neither a Pass nor the Ellipsis placeholder). Messages are
# suppressed on purpose so this file has no expected output.
# pylint: disable=too-many-statements
def single_return():
    return 1


def pass_with_real_work():
    pass  # noqa: PIE790 - this pass is the control case, keep it
    return 1
