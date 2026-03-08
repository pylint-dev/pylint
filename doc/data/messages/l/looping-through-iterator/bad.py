gen_ex = (x for x in range(3))
for _i in range(2):
    for item in gen_ex:  # [looping-through-iterator]
        print(item)