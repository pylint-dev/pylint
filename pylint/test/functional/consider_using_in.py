# pylint: disable=missing-docstring, invalid-name, pointless-statement, misplaced-comparison-constant, undefined-variable, literal-comparison

value = value1 = 1
value2 = 2
a_set = {1, 2, 3}
a_list = [1, 2, 3]
a_str = '1'

# Positive
value == 1 or value == 1  # [consider-using-in]
value == 1 or value == 2  # [consider-using-in]
value == 1 or value == undef_value  # [consider-using-in]
value == 1 or value == 2 or value == 3  # [consider-using-in]
value == '1' or value == '2'  # [consider-using-in]
1 == value or 2 == value  # [consider-using-in]
1 == value or value == 2  # [consider-using-in]
value == 1 or value == a_list  # [consider-using-in]
value == a_set or value == a_list or value == a_str  # [consider-using-in]
value != 1 and value != 2  # [consider-using-in]
value in (1, 2) or value in (3, 4)  # [consider-using-in]
value == 1 or value in (2, 3)  # [consider-using-in]
value != 1 and value not in (2, 3)  # [consider-using-in]
value1 == value2 or value2 == value1  # [consider-using-in]
(value1 == 1 or value1 == 2) and (value2 != 1 and value2 != 2)  # [consider-using-in]

# Negative
value != 1 or value != 2  # not a "not in"-case because of "or"
value == 1 and value == 2  # not a "in"-case because of "and"
value == 1 and value == 2 or value == 3  # not only 'or's
value == 1 or value == 2 or 3 < value < 4  # not only '=='
value == 1  # value not checked against multiple values
value == 1 and value in (2, 3)  # unjoinable "and" and "in"
value == 1 or value == 2 or value == 3 and value == 4  # not all checks are concatenated with 'or'
value == 1 or value in (2, 3) and value == 4  # not all checks are concatenated with 'or'
value == 1 or 2 < value < 3  # length of 'ops' != 1 for second check
value == 1 or (value == 2 or value == 3)  # could be considered in the future, but too complex for now
value is 1 or value is 2  # 'in' compares using '==' not 'is' and therefore not considered
not value == 1 and not value == 2
value1 == 1 or value2 == 2  # different variables and only one comparison for each
value1 == value2 == 1 or value1 == 2  # not checking multi-compares for '=='
value1 != 1 == value2 and value2 != value1 != 2  # not checking multi-compares for '!='
value1 == 1 or value2 in (2, 3)  # unjoinable 'value1' != 'value2'
value1 == 1 or value1 == value2 or value2 == 3  # value1 or value2 do not occur in every check
value1 == 1 or value1 == 2 or value2 == 1 or value2 == 2  # value1 or value2 do not occur in every check
