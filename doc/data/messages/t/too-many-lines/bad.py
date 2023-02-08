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

print(leap_year(1990))
print(leap_year(1991))
print(leap_year(1992))
print(leap_year(1993))
print(leap_year(1994))
