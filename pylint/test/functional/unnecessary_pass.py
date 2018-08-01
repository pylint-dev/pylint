# pylint: disable=missing-docstring, too-few-public-methods

try:
    A = 2
except ValueError:
    A = 24
    pass # [unnecessary-pass]

def docstring_only():
    '''In Python, stubbed functions often have a body that contains just a
    single `pass` statement, indicating that the function doesn't do
    anything. However, a stubbed function can also have just a
    docstring, and function with a docstring and no body also does
    nothing.
    '''


# This function has no docstring, so it needs a `pass` statement.
def pass_only():
    pass


def docstring_and_pass():
    '''This function doesn't do anything, but it has a docstring, so its
    `pass` statement is useless clutter.

    NEW CHECK: useless-pass

    This would check for stubs with both docstrings and `pass`
    statements, suggesting the removal of the useless `pass`
    statements
    '''
    pass # [unnecessary-pass]


class DocstringOnly:
    '''The same goes for class stubs: docstring, or `pass`, but not both.
    '''


# No problem
class PassOnly:
    pass


class DocstringAndPass:
    '''Whoops! Mark this one as bad too.
    '''
    pass # [unnecessary-pass]
