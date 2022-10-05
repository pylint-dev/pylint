import random

MAX_NUM_OF_ITERATIONS = 5
THRESHOLD_VAL = 100
MIN_MEASUREMENT_VAL = 0
MAX_MEASUREMENT_VAL = 200

measurement = random.randint(MIN_MEASUREMENT_VAL, MAX_MEASUREMENT_VAL)
above_threshold = False
i = 0
while i < MAX_NUM_OF_ITERATIONS:
    above_threshold = measurement > THRESHOLD_VAL
    if above_threshold:
        break
    measurement = random.randint(MIN_MEASUREMENT_VAL, MAX_MEASUREMENT_VAL)
