# pylint: disable=missing-docstring,invalid-name,undefined-variable,multiple-statements

# Variations of 'result'
result = ''
for number in ['1', '2', '3']:
    result += number  # [consider-using-join]

result = 'header'
for number in ['1', '2', '3']:
    result += number  # [consider-using-join]

result = another_result = ''
for number in ['1', '2', '3']:
    result += number  # [consider-using-join]

another_result = result = ''
for number in ['1', '2', '3']:
    result += number  # [consider-using-join]

result = 0  # result is not a string
for number in ['1', '2', '3']:
    result += number

RESULT = ''  # wrong name / initial variable missing
for number in ['1', '2', '3']:
    result += [number]

string_variable = ''
result = string_variable  # type of 'result' not obviously a string
for number in ['1', '2', '3']:
    result += number

result = ''
another_result = ''  # result defined too early
for number in ['1', '2', '3']:
    result += [number]

for number in ['1', '2', '3']:  # 'result'-definition missing
    result += number


# Variations of 'number'
result = ''  # no concatenation (iterator-name differs)
for name in ['1', '2', '3']:
    result += number

result = ''  # no concatenation (iterator-name differs)
for _ in ['1', '2', '3']:
    result += number
# 'exprlist' is not a single name
for index, number in ['1', '2', '3']:
    result += number


# Variations of 'iterable'
result = ''
for number in []:
    result += number  # [consider-using-join]

result = ''
for number in "a text":
    result += number  # [consider-using-join]

result = ''
for number in [1, 2, 3]:
    result += number  # [consider-using-join]

a_list = [1, 2, 3]
result = ''
for number in a_list:
    result += number  # [consider-using-join]

result = ''
for number in ['1', '2', '3']:
    result += number  # [consider-using-join]

result = ''
for number in undefined_iterable:
    result += number  # [consider-using-join]


# Variations of loop-body
result = ''  # addition is not the only part of the body
for number in ['1', '2', '3']:
    print(number)
    result += number

result = ''  # addition is not the only part of the body
for number in ['1', '2', '3']:
    result += number
    print(number)

result = ''  # augmented addition is not a simple one
for number in ['1', '2', '3']:
    result += '4' + number

result = ''  # assignment is not augmented
for number in ['1', '2', '3']:
    result = number

result = ''  # augmented assignment is not an addition
for number in ['1', '2', '3']:
    result -= number

result = ''  # addition is not the 'number'-iterable
for number in ['1', '2', '3']:
    result += another_number

result = ''
for number in ['1', '2', '3']: result += number  # [consider-using-join]

result = ''
for number in ['1']:
    result.result += number

# Does not emit if the body is more complex
result = {'context': 1}
result['context'] = 0
for number in ['1']:
    result1 = 42 + int(number)
    result['context'] += result1 * 24

# Does not crash if the previous sibling does not have AssignNames
result['context'] = 0
for number in ['1']:
    result['context'] += 24
