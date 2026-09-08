def baskets_hold_the_same(red, green):
    # Each basket holds at least as many apples as the other, so the two
    # baskets hold the same number.
    return red >= green and green >= red  # [chained-comparison-all-equal]
