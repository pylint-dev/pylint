"""PEP 798 unpacking checks that the unpacked element is iterable."""
# pylint: disable=missing-function-docstring
NESTED = [[1, 2], [3, 4]]
NUMBERS = [1, 2, 3]

FLAT_LIST = [*sub for sub in NESTED]
FLAT_SET = {*sub for sub in NESTED}
FLAT_GEN = list(*sub for sub in NESTED)

BAD_LIST = [*number for number in NUMBERS]  # [not-an-iterable]
BAD_SET = {*number for number in NUMBERS}  # [not-an-iterable]
BAD_GEN = list(*number for number in NUMBERS)  # [not-an-iterable]


async def lists():
    yield [1, 2]


async def numbers():
    yield 1


async def unpack_async():
    flat = [*sub async for sub in lists()]
    # The value yielded by an 'async for' cannot be inferred, so the
    # non-iterable element goes unreported instead of being a false positive.
    unreported = [*number async for number in numbers()]
    return flat, unreported
