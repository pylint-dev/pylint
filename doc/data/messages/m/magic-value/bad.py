import random

measurement = random.randint(0, 200)
above_threshold = False
i = 0
while i < 5:   # [magic-value-compare]
    above_threshold = measurement > 100   # [magic-value-compare]
    if above_threshold:
        break
    measurement = random.randint(0, 200)
