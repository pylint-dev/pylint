import random


def is_it_a_good_day():
    return random.choice([True, False])


if is_it_a_good_day:  # [missing-parentheses-for-call-in-test]
    print("Today is a good day!")
