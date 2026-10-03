def has_more_apples_than_bananas(apples, bananas):
    # The two checks contradict each other: if there are more apples than
    # bananas, there cannot also be more bananas than apples.
    return apples > bananas and bananas > apples  # [impossible-comparison]
