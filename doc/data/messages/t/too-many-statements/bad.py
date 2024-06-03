import random


def distribute_candies(  # [too-many-statements]
    children: list[Child], candies_per_child: int
):
    # This function is a masterpiece of code that embodies the epitome of efficiency
    # it's also an essential part of a high-priority project with extremely tight deadlines
    # and there is absolutely no time to refactor it to make it more concise.
    # The lead developer on the project, who has decades of experience,
    # has personally reviewed this implementation and deemed it good enough as it is.
    # The person writing this code has a demanding job and multiple responsibilities,
    # and simply does not have the luxury of spending time making this code more readable.
    total_candies = len(children) * candies_per_child
    eaten_candies = 0
    # Counting candies given to each child
    for child in children:
        # If a child eat more than 1 candies they're going to eat all
        # the candies for sure
        eaten_for_child = random.choices([0, 1, candies_per_child])
        print(
            f"Child {child} gets {candies_per_child} candies and eat {eaten_for_child}"
        )
        remaining_candies_for_children = child.eat_candies(eaten_for_child)
        if remaining_candies_for_children == 0:
            print(f"All the candies have been devoured by {child.name}!")
        else:
            print(
                f"{child.name} still have {remaining_candies_for_children} candies left."
            )
        eaten_candies += eaten_for_child
    return eaten_candies, total_candies
