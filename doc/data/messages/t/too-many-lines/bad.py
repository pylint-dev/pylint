def leap_year(year): # [too-many-lines]
    """ Function used to determine whether a given year is a leap year """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False

for year in range(1990, 2000):
    print(leap_year(year))

    if leap_year(year):
        print(str(year) + " was a leap year")
    else:
        print(str(year) + " was not a leap year")
