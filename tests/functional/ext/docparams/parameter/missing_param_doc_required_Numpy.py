"""Tests for missing-param-doc and missing-type-doc for Numpy style docstrings
with accept-no-param-doc = no
"""
# pylint: disable=invalid-name, unused-argument, undefined-variable
# pylint: disable=line-too-long, too-few-public-methods, missing-class-docstring
# pylint: disable=missing-function-docstring, function-redefined, inconsistent-return-statements


def test_missing_func_params_in_numpy_docstring(  # [missing-param-doc, missing-type-doc]
    x, y, z
):
    """Example of a function with missing NumPy style parameter
        documentation in the docstring

    Parameters
    ----------
    x:
        bla
    z: int
        bar

    some other stuff
    """


class Foo:
    def test_missing_method_params_in_numpy_docstring(  # [missing-param-doc, missing-type-doc]
        self, x, y
    ):
        """Example of a class method with missing parameter documentation in
        the Numpy style docstring

        missing parameter documentation

        Parameters
        ----------
        x:
            bla
        """
