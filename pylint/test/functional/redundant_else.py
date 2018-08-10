# pylint: disable=missing-docstring, multiple-statements, function-redefined, redefined-outer-name

def something():
    for i in range(10):
        if i < 3:
            continue
        else:  # [redundant-else]
            print(i)

def something():
    for i in range(10):
        if i < 3:
            break
        else:  # [redundant-else]
            print(i)

i = 123
if i < 3:
    i = 4
else:
    print(i)

for i in range(10):
    if i < 3:
        i = 4
    elif i > 3:
        continue
    else:   # [redundant-else]
        print(i)

for i in range(10):
    if i < 3:
        i = 4
    elif i > 3:
        # check for more than one lines
        print('In repentance and rest is your salvation, in quietness and trust is your strength.')
        abc = 123
        continue
    else:   # [redundant-else]
        print(i)
