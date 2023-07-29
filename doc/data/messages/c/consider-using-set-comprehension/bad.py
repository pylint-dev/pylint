NUMBERS = [1, 2, 2, 3, 4, 4]

# +1: [consider-using-set-comprehension]
UNIQUE_EVEN_NUMBERS = set([number for number in NUMBERS if number % 2 == 0])
