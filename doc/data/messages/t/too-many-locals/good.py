from typing import NamedTuple

from childhood import Child, Sweet


class SweetDistrubutionCharacteristics(NamedTuple):
    number_of_sweets: int
    number_of_sweet_per_child: int
    number_of_children: int

    @property
    def sweets_given(self):
        return self.number_of_sweet_per_child * self.number_of_children


def handle_sweets(infos):
    children = [Child(info) for info in infos]
    characteristics = SweetDistrubutionCharacteristics(87, 5, len(children))
    _allocate_sweets_to_children(children, characteristics)
    financial_impact = _assess_financial_impact(characteristics)
    print(f"{children} ate {financial_impact}")


def _allocate_sweets_to_children(
    children, characteristics: SweetDistrubutionCharacteristics
) -> None:
    sweets = [Sweet() * characteristics.number_of_sweets]
    for child in children:
        child.give(sweets[characteristics.number_of_sweet_per_child :])


def _assess_financial_impact(characteristics: SweetDistrubutionCharacteristics) -> str:
    time_to_eat_sweet = 54
    money = 45.0
    price_of_sweet = 0.42
    cost_of_children = characteristics.sweets_given * price_of_sweet
    remaining_money = money - cost_of_children
    time_it_took_assuming_parallel_eating = (
        time_to_eat_sweet * characteristics.number_of_sweet_per_child
    )
    return (
        f"{cost_of_children}¤ of sweets in "
        f"{time_it_took_assuming_parallel_eating}, you still have {remaining_money}"
    )
