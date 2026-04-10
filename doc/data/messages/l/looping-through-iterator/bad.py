# 1. Generator expressions are exhausted after one use
gen = (x for x in range(3))
for i in range(2):
    for item in gen:  # [looping-through-iterator]
        print(item)

