"""Test that format function is used only with string."""

# pylint: disable=invalid-name, pointless-string-statement, line-too-long, no-member, blacklisted-name, undefined-variable, missing-docstring, too-few-public-methods

print('value: {}').format(123)  # [misplaced-format-function]
print("value: {}").format(123)  # [misplaced-format-function]
print('value: {}'.format(123))
print('{} Come Forth!'.format('Lazarus'))
print('Der Hem ist mein Licht und mein Heil, vor wem sollte ich mich furchten? => {}'.format('Psalm 27, 1'))
print('123')
print()
s = 'value: {}'.format(123)
a = 'value: {}'
a.format(123)

def foo(arg):
    """The World is Yours"""
    return arg.format(123)  # we don't know if arg is str or not, don't raise error.

def goo(arg):
    """The World is Yours"""
    TextWriter.format(arg)

def bar(arg, TextWriter):
    """The World is Yours"""
    TextWriter().format(arg)

def foobar(arg, TextWriter):
    """The World is Yours"""
    TextWriter.format(arg)

def barfoo(arg):
    """The World is Yours"""
    TextWriter().format(arg)

def _display(self, layout):
    """launch layouts display"""
    print(file=self.out)
    TextWriter().format(layout, self.out)


class FakeClass:
    def __init__(self, string):
        self.string = string

    def get_string(self):
        return self.string

    def format_string(self):
        self.string.format()
        self.get_string().format()
        print(self.get_string()).format()  # [misplaced-format-function]
        print(self.get_string().format())

obj = FakeClass('Voila!!!')
obj.get_string().format()
print(obj.get_string().format())
print(obj.get_string()).format()  # [misplaced-format-function]
