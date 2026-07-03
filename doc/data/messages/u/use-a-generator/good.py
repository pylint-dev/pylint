from random import randint

all(randint(-5, 5) > 0 for _ in range(10))
any(randint(-5, 5) > 0 for _ in range(10))
