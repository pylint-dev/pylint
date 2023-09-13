import random

measurement = random.randint(0, 200)
above_threshold = False
i = 0
while i < 5:  # [magic-value-comparison]
    above_threshold = measurement > 100  # [magic-value-comparison]
    if above_threshold:
        break
    measurement = random.randint(0, 200)
