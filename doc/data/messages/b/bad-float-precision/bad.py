huge_number = 1.5e500  # [bad-float-precision]  # overflows to math.inf
tiny_number = 1e-1000  # [bad-float-precision]  # underflows to 0.0

# 21 significant figure, more than 15, resolves to 3.141592653589793
pi = 3.14159265358979323846  # [bad-float-precision]
