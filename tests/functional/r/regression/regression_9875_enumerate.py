"""https://github.com/pylint-dev/pylint/issues/9875"""
# value = 0
for idx, value in enumerate(iterable=[1, 2, 3]):
    print(f'{idx=} {value=}')
# +1: [undefined-loop-variable, undefined-loop-variable]
for idx, value in enumerate(iterable=[value-1, value-2*1]):
    print(f'{idx=} {value=}')
