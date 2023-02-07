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

if leap_year(2020):
    print(str(2020) + " was a leap year")
else:
    print(str(2020) + " was not a leap year")

if leap_year(2021):
    print(str(2021) + " was a leap year")
else:
    print(str(2021) + " was not a leap year")
