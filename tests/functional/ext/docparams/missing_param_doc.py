#pylint: disable=missing-module-docstring, too-few-public-methods


from typing import overload, Union


def foobar1(arg1, arg2): #[missing-any-param-doc]
    """function foobar ...
    """
    print(arg1, arg2)

def foobar2(arg1, arg2): #[missing-any-param-doc]
    """function foobar ...
    Parameters
    ----------
    """
    print(arg1, arg2)

def foobar3(arg1, arg2, arg3): #[missing-param-doc, missing-type-doc]
    """function foobar ...
    Parameters
    ----------
    arg1: int
    arg3: float
    """
    print(arg1, arg2, arg3)

def foobar4(arg1, arg2): #[missing-param-doc, missing-type-doc]
    """function foobar ...
    Parameters
    ----------
    arg1: int
        description
    """
    print(arg1, arg2)

def foobar5(arg1, arg2): #[missing-type-doc]
    """function foobar ...
    Parameters
    ----------
    arg1:
        description
    arg2: str
    """
    print(arg1, arg2)

def foobar6(arg1, arg2, arg3): #[missing-param-doc, missing-type-doc]
    """function foobar ...
    Parameters
    ----------
    arg1: int
        description
    arg2: int
    """
    print(arg1, arg2, arg3)

def foobar7(arg1, arg2): #[missing-any-param-doc]
    """function foobar ...
    Parameters
    ----------
    arg1
    """
    print(arg1, arg2)

def foobar8(arg1): #[missing-any-param-doc]
    """function foobar"""

    print(arg1)

def foobar9(arg1, arg2, arg3):
    """function foobar ...
    Parameters
    ----------
    arg1: int
    arg2: int
    arg3: str
    """
    print(arg1, arg2, arg3)

def foobar10(arg1, arg2, arg3): #[missing-type-doc]
    """function foobar ...
    Parameters
    ----------
    arg1:
        desc1
    arg2: int
    arg3:
        desc3
    """
    print(arg1, arg2, arg3)

def foobar11(arg1, arg2): #[missing-any-param-doc]
    """function foobar ...
    Args
    ----------
    arg1
    arg2
    """
    print(arg1, arg2)

def foobar12(arg1, arg2, arg3): #[missing-param-doc, missing-type-doc]
    """function foobar ...
    Args
    ----------
    arg1: int
    arg2:
        does something
    arg3
    """
    print(arg1, arg2, arg3)

def foobar13(arg1, *args, arg3=";"):
    """Description of the function

    Parameters
    ----------
    arg1 : str
        Path to the input.
    *args :
        Relevant parameters.
    arg3 : str, optional
        File separator.
    """
    print(arg1, args, arg3)

def foobar14(arg1, *args):
    """Description of the function

    Parameters
    ----------
    arg1 : str
        Path to the input.
    *args :
        Relevant parameters.
    """
    print(arg1, args)

def foobar15(*args):
    """Description of the function

    Parameters
    ----------
    *args :
        Relevant parameters.
    """
    print(args)


def foobar16(one: int, two: str, three: float) -> int:
    """Description of the function

    Args:
        one: A number.
        two: Another number.
        three: Yes another number.

    Returns:
        The number one.
    """
    print(one, two, three)
    return 1


def foobar17(one, two, three):
    # type: (int, str, float) -> int
    """Description of the function

    Args:
        one: A number.
        two: Another number.
        three: Yes another number.

    Returns:
        The number one.
    """
    print(one, two, three)
    return 1


def foobar18(
    one,  # type: int
    two,  # type: str
    three,  # type: float
):
    # type: (...) -> int
    """Description of the function

    Args:
        one: A number.
        two: Another number.
        three: Yes another number.

    Returns:
        The number one.
    """
    print(one, two, three)
    return 1


def foobar19(one, two, **kwargs):
    # type: (int, str, float) -> int
    """Description of the function

    Args:
        one: A number.
        two: Another number.
        kwargs: More numbers.

    Returns:
        The number one.
    """
    print(one, two, kwargs)
    return 1


class Word:
    """
    Methods decorated with `typing.overload` are excluded
    from the docparam checks. For example: `missing-param-doc` and
    `missing-type-doc`.
    """
    def __init__(self, word):
        self.word = word

    @overload
    def starts_with(self, letter: None) -> None: ...

    @overload
    def starts_with(self, letter: str) -> bool: ...

    def starts_with(self, letter: Union[str, None]) -> Union[bool, None]:
        """
        Returns:
            True if `self.word` begins with `letter`

        Args:
            letter: str
        """
        if self.word:
            return self.word.startswith(letter)
        return None
