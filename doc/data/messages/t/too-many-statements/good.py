import random


def distribute_candies(children: list[Child], candies_per_child: int):
    total_candies = len(children) * candies_per_child
    eaten_candies = 0
    for child in children:
        eaten_candies += _distribute_candies_to_child(candies_per_child, child)
    return eaten_candies, total_candies


def _distribute_candies_to_child(candies_per_child: int, child: Child):
    # If a child eat more than 1 candies they're going to eat all
    # the candies for sure
    eaten_for_child = random.choices([0, 1, candies_per_child])
    print(f"Child {child} gets {candies_per_child} candies and eat {eaten_for_child}")
    remaining_candies_for_children = child.eat_candies(eaten_for_child)
    if remaining_candies_for_children == 0:
        print(f"All the candies have been devoured by {child.name}!")
    else:
        print(f"{child.name} still have {remaining_candies_for_children} candies left.")
    return eaten_for_child
