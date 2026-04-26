huge_number = 1.5e500  # [bad-number-notation]  # overflows to math.inf
tiny_number = 1e-1000  # [bad-number-notation]  # underflows to 0.0
many_digits = 486787299458.15656  # [bad-number-notation]  # 17 sig figs > 15
