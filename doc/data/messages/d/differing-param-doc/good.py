def leapYear(year):
    """ Function used to determine if a given year is a leap year
        :param int year: a year to check is a leap year
        :returns: a result.
        :rtype: boolean """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False
