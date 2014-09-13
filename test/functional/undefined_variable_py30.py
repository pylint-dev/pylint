"""Test warnings about access to undefined variables
for various Python 3 constructs. """
# pylint: disable=too-few-public-methods, no-init, no-self-use

class Undefined:
    """ test various annotation problems. """

    def test(self)->Undefined: # [undefined-variable]
        """ used Undefined, which is Undefined in this scope. """

    Undefined = True

    def test1(self)->Undefined:
        """ This Undefined exists at local scope. """

    def test2(self):
        """ This should not emit. """
        def func()->Undefined:
            """ empty """
            return
        return func


class Undefined1:
    """ Other annotation problems. """

    Undef = 42
    ABC = 42

    class InnerScope:
        """ Test inner scope definition. """

        def test_undefined(self)->Undef: # [undefined-variable]
            """ Looking at a higher scope is impossible. """

        def test1(self)->ABC: # [undefined-variable]
            """ Triggers undefined-variable. """
