NUMBERS = [1, 2, 3]

# +1: [consider-using-dict-comprehension]
DOUBLED_NUMBERS = dict([(number, number * 2) for number in NUMBERS])
