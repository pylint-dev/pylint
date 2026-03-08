gen_ex = (x for x in range(3))
list_ex = list(gen_ex)
for _i in range(2):
    for item in list_ex:
        print(item)
