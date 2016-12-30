# pylint: disable=missing-docstring,too-few-public-methods,no-member,import-error,no-self-use,redefined-outer-name,invalid-name,unused-variable

from unknown import Unknown

FILE_NAME = 'file_name'


class CustomClass(object):
    def xreadlines(self):
        return []


for line in Unknown().xreadlines():
    pass
for line in Unknown.xreadlines():
    pass
for line in file.xreadlines():
    pass
for line in CustomClass().xreadlines():
    pass
for char in file(FILE_NAME).read():
    pass

COMP = [line for line in file(FILE_NAME)]
COMP = (line for line in file(FILE_NAME))
COMP = {line for line in file(FILE_NAME)}
COMP = {line: line for line in file(FILE_NAME)}
COMP = [line for line in file(FILE_NAME).xreadlines()]  # [consider-iterating-file]
COMP = (line for line in file(FILE_NAME).xreadlines())  # [consider-iterating-file]
COMP = {line for line in file(FILE_NAME).xreadlines()}  # [consider-iterating-file]
COMP = {line: line for line in file(FILE_NAME).xreadlines()}  # [consider-iterating-file]

for line in file(FILE_NAME).xreadlines():  # [consider-iterating-file]
    pass

for line in file(FILE_NAME):
    pass

with file(FILE_NAME) as fh:
    for line in fh.xreadlines():  # [consider-iterating-file]
        pass

with file(FILE_NAME) as fh:
    for line in fh:
        pass

with file(FILE_NAME) as fh:
    COMP = [line for line in fh.xreadlines()]  # [consider-iterating-file]

with file(FILE_NAME) as fh:
    COMP = [line for line in fh]

with file(FILE_NAME) as fh:
    COMP = (line for line in fh.xreadlines())  # [consider-iterating-file]

with file(FILE_NAME) as fh:
    COMP = (line for line in fh)

with file(FILE_NAME) as fh:
    COMP = {line for line in fh.xreadlines()}  # [consider-iterating-file]

with file(FILE_NAME) as fh:
    COMP = {line for line in fh}

with file(FILE_NAME) as fh:
    COMP = {line: line for line in fh.xreadlines()}  # [consider-iterating-file]

with file(FILE_NAME) as fh:
    COMP = {line: line for line in fh}

MY_LINES_GENERATOR = file(FILE_NAME).xreadlines()

with file(FILE_NAME) as fh:
    MY_LINES_GENERATOR = fh.xreadlines()

with file(FILE_NAME) as fh1, file('another') as fh2:
    COMP = [line for line in fh1.xreadlines()]  # [consider-iterating-file]
    COMP2 = [line for line in fh2]


def non_builtin_file():
    # pylint: disable=redefined-builtin,redefined-outer-name
    from somewhere import file
    return [line for line in file(FILE_NAME).xreadlines()]


def file_without_ctxmgr():
    fh = file(FILE_NAME)
    for line in fh.xreadlines():  # [consider-iterating-file]
        pass
    fh.close()
