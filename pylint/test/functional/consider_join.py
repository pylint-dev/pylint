# pylint: disable=missing-docstring,invalid-name,undefined-variable,multiple-statements

# Variations of 'result'
result1 = ''
for number in ['1', '2', '3']:
    result1 += number  # [consider-using-join]

result2 = 'header'
for number in ['1', '2', '3']:
    result2 += number  # [consider-using-join]

result3 = another_result3 = ''
for number in ['1', '2', '3']:
    result3 += number  # [consider-using-join]

another_result4 = result4 = ''
for number in ['1', '2', '3']:
    result4 += number  # [consider-using-join]

result5 = 0
for number in ['1', '2', '3']:
    result5 += number  # result is not a string

RESULT6 = ''
for number in ['1', '2', '3']:
    result6 += number  # wrong name / initial variable missing

string_variable7 = ''
result7 = string_variable7
for number in ['1', '2', '3']:
    result7 += number  # [consider-using-join]

result8 = ''
another_result8 = ''
for number in ['1', '2', '3']:
    result8 += number  # [consider-using-join]

for number in ['1', '2', '3']:
    result9 += number  # 'result'-definition missing


# Variations of 'loop-variable'
result10 = ''
for name in ['1', '2', '3']:
    result10 += number  # no concatenation (iterator-name differs)

result11 = ''
for _ in ['1', '2', '3']:
    result11 += number  # no concatenation (iterator-name differs)

result12 = ''
for index, number in ['1', '2', '3']:
    result12 += number  # 'exprlist' is not a single name


# Variations of 'iterable'
result13 = ''
for number in []:
    result13 += number  # iterable does not contain strings

result14 = ''
for number in "a text":
    result14 += number  # would be a [consider-using-join], but type str was uninferrable

result15 = ''
for number in [1, 2, 3]:
    result15 += number  # iterable does not contain strings

a_list = [1, 2, 3]
result16 = ''
for number in a_list:
    result16 += number  # iterable does not contain strings

result17 = ''
for number in ['1', '2', '3']:
    result17 += number  # [consider-using-join]

result18 = ''
for number in undefined_iterable:
    result18 += number  # iterable does not contain strings


# Variations of loop-body
result19 = ''
for number in ['1', '2', '3']:
    print(number)
    result19 += number  # addition is not the only part of the body

result20 = ''
for number in ['1', '2', '3']:
    result20 += number  # addition is not the only part of the body
    print(number)

result21 = ''
for number in ['1', '2', '3']:
    result21 += '4' + number  # augmented addition is not a simple one

result22 = ''
for number in ['1', '2', '3']:
    result22 = number  # assignment is not augmented

result23 = ''
for number in ['1', '2', '3']:
    result23 -= number  # augmented assignment is not an addition

result24 = ''
for number in ['1', '2', '3']:
    result24 += another_number  # addition is not the 'number'-iterable

result26 = ''
for number in ['1', '2', '3']: result26 += number  # [consider-using-join]


# Combinations of variations
result25 = ''
for number in [1, 2, 3]:
    result25 += str(number)  # generator expression would be necessary => ignored

result26 = 0
for number in "a text":
    result26 += number  # plus is not a string concatenation
