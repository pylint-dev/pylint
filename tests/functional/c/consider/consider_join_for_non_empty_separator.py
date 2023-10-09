# pylint: disable=missing-docstring,invalid-name,undefined-variable,multiple-statements

result = 'a'
for number in ['1', '2', '3']:
    result += f'b{number}'
assert result == 'ab1b2b3'
assert result == 'b'.join(['a', '1', '2', '3'])

result = 'a'
for number in ['1', '2', '3']:
    result += f'{number}c'
assert result == 'a1c2c3c'
assert result == 'a' + 'c'.join(['1', '2', '3']) + 'c'

result = 'a'
for number in ['1', '2', '3']:
    result += f'b{number}c'
assert result == 'ab1cb2cb3c'
assert result == 'ab' + 'cb'.join(['1', '2', '3']) + 'c'

result = ''
for number in ['1', '2', '3']:
    result += f"{number}, "
result = result[:-2]
