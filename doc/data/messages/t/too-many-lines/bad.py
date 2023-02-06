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

print(leap_year(1900))
print(leap_year(1901))
print(leap_year(1902))
print(leap_year(1903))
print(leap_year(1904))
print(leap_year(1905))
print(leap_year(1906))
print(leap_year(1907))
print(leap_year(1908))
print(leap_year(1909))
print(leap_year(1910))
print(leap_year(1911))
print(leap_year(1912))
print(leap_year(1913))
print(leap_year(1914))
print(leap_year(1915))
print(leap_year(1916))
print(leap_year(1917))
print(leap_year(1918))
print(leap_year(1919))
print(leap_year(1920))
print(leap_year(2004))
