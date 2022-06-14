def find_even_number(numbers):
    for x in numbers:
        if x % 2 == 0:
            return x
    print("Did not find an even number")
