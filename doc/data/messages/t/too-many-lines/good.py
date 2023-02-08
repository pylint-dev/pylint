def leap_year(year):
    """ Function used to determine whether a given year is a leap year """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False

for year in range(1990, 1994):
    print(leap_year(year))
