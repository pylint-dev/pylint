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

print(leap_year(1900))
print(leap_year(1901))
print(leap_year(1902))
print(leap_year(1903))
print(leap_year(1904))
print(leap_year(1905))
print(leap_year(1906))
print(leap_year(1907))
