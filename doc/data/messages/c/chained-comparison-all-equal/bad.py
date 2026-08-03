def in_thermal_equilibrium(a, b, c):
    # Heat only flows from hotter to colder bodies, so a cycle of ``>=``
    # between three temperatures forces all three to be equal.
    return a >= b and b >= c and c >= a  # [chained-comparison-all-equal]
