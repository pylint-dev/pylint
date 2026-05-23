# pylint: disable=missing-docstring, invalid-name, unused-argument, consider-using-sys-exit, no-else-return
"""Test that quit() and exit() are handled consistently with sys.exit()"""

import sys

# These functions should not trigger inconsistent-return-statements
# because quit, exit, and sys.exit are never-returning functions (#10508)

def func_with_quit_1(i):
    """quit() in else branch should be treated like sys.exit()"""
    if i == 1:
        return i
    quit(1)

def func_with_quit_2(i):
    """quit() in if branch should be treated like sys.exit()"""
    if i == 1:
        quit(1)
    return 1

def func_with_exit_1(i):
    """exit() in else branch should be treated like sys.exit()"""
    if i == 1:
        return i
    exit(1)

def func_with_exit_2(i):
    """exit() in if branch should be treated like sys.exit()"""
    if i == 1:
        exit(1)
    return 1

def func_with_sys_exit_1(i):
    """sys.exit() in else branch - baseline test"""
    if i == 1:
        return i
    sys.exit(1)

def func_with_sys_exit_2(i):
    """sys.exit() in if branch - baseline test"""
    if i == 1:
        sys.exit(1)
    return 1

# Test mixed usage
def func_mixed_exit_methods(i):
    """Using different exit methods should all work consistently"""
    if i == 1:
        return "one"
    if i == 2:
        quit()
    if i == 3:
        exit()
    sys.exit()

# This should trigger inconsistent-return-statements
def func_inconsistent_example(i):  # [inconsistent-return-statements]
    """This should trigger the warning as a negative test case"""
    if i == 1:
        return i
    print("Not exiting, just printing")
