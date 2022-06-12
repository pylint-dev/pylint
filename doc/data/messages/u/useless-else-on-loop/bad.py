def find_even_number(lst):
    for x in lst:
        if x % 2 == 0:
            return x
    else:  # [useless-else-on-loop]
        print("Did not find an even number")
