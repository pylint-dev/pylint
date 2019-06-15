# pylint: disable=missing-docstring,invalid-name,using-constant-test,invalid-sequence-index,undefined-variable
dictionary = dict()
key = 'key'

if 'key' in dictionary:  # [consider-using-get]
    variable = dictionary['key']

if 'key' in dictionary:  # [consider-using-get]
    variable = dictionary['key']
else:
    variable = 'default'

if key in dictionary:  # [consider-using-get]
    variable = dictionary[key]

if 'key' in dictionary:  # not accessing the dictionary in assignment
    variable = "string"

if 'key' in dictionary:  # is a match, but not obvious and we ignore it for now
    variable = dictionary[key]

if 'key1' in dictionary:  # dictionary querried for wrong key
    variable = dictionary['key2']

if 'key' in dictionary:  # body is not pure
    variable = dictionary['key']
    print('found')

if 'key' in dictionary:  # body is not pure
    variable = dictionary['key']
    print('found')
else:
    variable = 'default'

if 'key' in dictionary1:  # different dictionaries
    variable = dictionary2['key']
else:
    variable = 'default'

if 'key' in dictionary:  # body is not pure
    variable = dictionary['key']
else:
    variable = 'default'
    print('found')

if 'key' in dictionary:  # different variables
    variable1 = dictionary['key']
else:
    variable2 = 'default'

if 'key' in dictionary:  # assignment is not simple
    variable1 = variable2 = dictionary['key']

if 'key' in dictionary:  # assignment is not simple
    variable1 = dictionary['key']
else:
    variable1 = variable2 = "default"

if 'word' in 'text':
    variable = 'text'['word']  # already bogus, but to assert that this only works with dictionaries

if 'word' in dictionary:
    variable = 'dictionary'['word']

if 'key1' in dictionary:  # not the simple case
    variable = dictionary['key1']
elif 'key2' in dictionary:  # [consider-using-get]
    variable = dictionary['key2']
else:
    variable = 'default'

if 'key' in dictionary and bool(key):  # not a simple compare
    variable = dictionary['key1']
else:
    variable = 'default'

if bool(key) and 'key' in dictionary:  # not a simple compare
    variable = dictionary['key1']
else:
    variable = 'default'


d1 = {'foo': None}
d2 = {}
# Cannot be represented as using .get()
if 'foo' in d1:
    d2['bar'] = d1['foo']

if 'key' in dictionary:
    variable = dictionary[1:]
