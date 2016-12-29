# pylint: disable=missing-docstring,too-few-public-methods,no-member,import-error,no-self-use,redefined-outer-name,invalid-name,unused-variable

from unknown import Unknown

FILE_NAME = 'file_name'


class CustomClass(object):
    def readlines(self):
        return []


for line in Unknown().readlines():
    pass
for line in Unknown.readlines():
    pass
for line in open.readlines():
    pass
for line in CustomClass().readlines():
    pass
for char in open(FILE_NAME).read():
    pass

COMP = [line for line in open(FILE_NAME)]
COMP = (line for line in open(FILE_NAME))
COMP = {line for line in open(FILE_NAME)}
COMP = {line: line for line in open(FILE_NAME)}
COMP = [line for line in open(FILE_NAME).readlines()]  # [consider-iterating-file]
COMP = (line for line in open(FILE_NAME).readlines())  # [consider-iterating-file]
COMP = {line for line in open(FILE_NAME).readlines()}  # [consider-iterating-file]
COMP = {line: line for line in open(FILE_NAME).readlines()}  # [consider-iterating-file]

for line in open(FILE_NAME).readlines():  # [consider-iterating-file]
    pass

for line in open(FILE_NAME):
    pass

with open(FILE_NAME) as fh:
    for line in fh.readlines():  # [consider-iterating-file]
        pass

with open(FILE_NAME) as fh:
    for line in fh:
        pass

with open(FILE_NAME) as fh:
    COMP = [line for line in fh.readlines()]  # [consider-iterating-file]

with open(FILE_NAME) as fh:
    COMP = [line for line in fh]

with open(FILE_NAME) as fh:
    COMP = (line for line in fh.readlines())  # [consider-iterating-file]

with open(FILE_NAME) as fh:
    COMP = (line for line in fh)

with open(FILE_NAME) as fh:
    COMP = {line for line in fh.readlines()}  # [consider-iterating-file]

with open(FILE_NAME) as fh:
    COMP = {line for line in fh}

with open(FILE_NAME) as fh:
    COMP = {line: line for line in fh.readlines()}  # [consider-iterating-file]

with open(FILE_NAME) as fh:
    COMP = {line: line for line in fh}

MY_LINES = open(FILE_NAME).readlines()

with open(FILE_NAME) as fh:
    MY_LINES = fh.readlines()

with open(FILE_NAME) as fh1, open('another') as fh2:
    COMP = [line for line in fh1.readlines()]  # [consider-iterating-file]
    COMP2 = [line for line in fh2]


def non_builtin_open():
    # pylint: disable=redefined-builtin
    from somewhere import open
    return [line for line in open(FILE_NAME).readlines()]


def open_without_ctxmgr():
    fh = open(FILE_NAME)
    for line in fh.readlines():  # [consider-iterating-file]
        pass
    fh.close()
