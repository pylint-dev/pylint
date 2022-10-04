from contextlib import ExitStack
with ExitStack() as stack:
    fh1 = stack.enter_context(open('file1.txt', 'w'))
    fh2 = stack.enter_context(open('file2.txt', 'w'))
