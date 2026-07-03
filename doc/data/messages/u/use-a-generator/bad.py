from random import randint

all([randint(-5, 5) > 0 for _ in range(10)])  # [use-a-generator]
any([randint(-5, 5) > 0 for _ in range(10)])  # [use-a-generator]
