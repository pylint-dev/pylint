from childhood import Child, Sweet


def main(infos):
    children = [Child(info) for info in infos]
    number_of_sweets = 87
    number_of_sweet_per_child = 5
    sweets_given = _allocate_sweets_to_children(
        children, number_of_sweets, number_of_sweet_per_child
    )
    financial_impact = _assess_financial_impact(number_of_sweet_per_child, sweets_given)
    print(f"{children} ate {financial_impact}")


def _assess_financial_impact(number_of_sweet_per_child, sweets_given):
    time_to_eat_sweet = 54
    money = 45.0
    price_of_sweet = 0.42
    cost_of_children = sweets_given * price_of_sweet
    remaining_money = money - cost_of_children
    time_it_too_assuming_parallel_eating = time_to_eat_sweet * number_of_sweet_per_child
    return (
        f"{cost_of_children}¤ of sweets in "
        f"{time_it_too_assuming_parallel_eating}, you still have {remaining_money}"
    )


def _allocate_sweets_to_children(children, number_of_sweets, number_of_sweet_per_child):
    sweets = [Sweet() * number_of_sweets]
    sweets_given = 0
    for child in children:
        sweets_given += number_of_sweet_per_child
        child.give(sweets[number_of_sweet_per_child:])
    return sweets_given
