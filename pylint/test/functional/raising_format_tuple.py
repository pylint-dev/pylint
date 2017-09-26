'''
Complain about multi-argument exception constructors where the first argument
contains a percent sign, thus suggesting a % string formatting was intended
instead.  The same holds for a string containing {...} suggesting str.format()
was intended.
'''

def bad_percent(arg):
    '''Raising a percent-formatted string and an argument'''
    raise KeyError('Bad key: %r', arg)  # [raising-format-tuple]

def good_percent(arg):
    '''Instead of passing multiple arguments, format the message'''
    raise KeyError('Bad key: %r' % arg)

def bad_multiarg(name, value):
    '''Raising a formatted string and multiple additional arguments'''
    raise ValueError('%s measures %.2f', name, value)  # [raising-format-tuple]

def good_multiarg(name, value):
    '''The arguments have to be written as a tuple for formatting'''
    raise ValueError('%s measures %.2f' % (name, value))

def bad_braces(arg):
    '''Curly braces as placeholders'''
    raise KeyError('Bad key: {:r}', arg)  # [raising-format-tuple]

def good_braces(arg):
    '''Call str.format() instead'''
    raise KeyError('Bad key: {:r}'.format(arg))

def bad_multistring(arg):
    '''Multiple adjacent string literals'''
    raise AssertionError(  # [raising-format-tuple]
        'Long message about %s '
        "split over several adjacent literals", arg)

def bad_triplequote(arg):
    '''String literals with triple quotes'''
    raise AssertionError(  # [raising-format-tuple]
        '''Long message about %s
        split over several adjacent literals''', arg)

def bad_unicode(arg):
    '''Unicode string literal'''
    raise ValueError(u'Bad %s', arg)  # [raising-format-tuple]

def raise_something_without_name(arg):
    '''Regression test for nodes without .node attribute'''
    import standard_exceptions  # pylint: disable=import-error
    raise standard_exceptions.MyException(u'An %s', arg)  # [raising-format-tuple]
