import random


def pick_one(item1, item2, item3, /):
    chosen_one = random.choice((item1, item2, item3))
    print(f"The chosen item is: {chosen_one}")

pick_one(item1="apple", item2="banana", item3="orange")  # [positional-only-arguments-expected]
