"""PEP 798 unpacking checks that the unpacked element is iterable."""
NESTED = [[1, 2], [3, 4]]
NUMBERS = [1, 2, 3]

FLAT_LIST = [*sub for sub in NESTED]
FLAT_SET = {*sub for sub in NESTED}
FLAT_GEN = list(*sub for sub in NESTED)

BAD_LIST = [*number for number in NUMBERS]  # [not-an-iterable]
BAD_SET = {*number for number in NUMBERS}  # [not-an-iterable]
BAD_GEN = list(*number for number in NUMBERS)  # [not-an-iterable]
