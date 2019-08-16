 # pylint: disable=no-self-use, no-method-argument, missing-docstring,


def function_3_args(first_argument, second_argument, third_argument):
    """three arguments function"""
    return first_argument, second_argument, third_argument


def function_default_arg(one=1, two=2):
    """fonction with default value"""
    return two, one


def args_out_of_order():
    """Tests for arguments-out-of-order"""
    first_argument = 1
    second_argument = 2
    third_argument = 3
    one = 1
    two = 2

    function_3_args(first_argument, third_argument, second_argument) # [arguments-out-of-order]
    function_3_args(second_argument, first_argument, # [arguments-out-of-order]
                    third_argument=third_argument)
    function_default_arg(two, one) # [arguments-out-of-order]

    # Checking exceptions:
    # supplying the same attribute twice instead of two different ones
    function_3_args(first_argument, first_argument, third_argument)

    # keyword passing
    function_default_arg(two=two, one=one)

    # anything other than named attributes
    function_3_args(1, list, 1 + 2)

    # The check assumes you know better if at least 1 arg does not match the function signature
    function_3_args(one, third_argument, second_argument)

    # we currently don't warn for the case where keyword args have been swapped
    function_default_arg(two=one, one=two)

    # ensure object methods are checked correctly despite implicit self
    class TestClass:
        @staticmethod
        def function_0_args():
            return
        def function_2_args(self, first_argument, second_argument=2):
            return first_argument, second_argument

    TestClass().function_2_args(second_argument, first_argument) # [arguments-out-of-order]
    TestClass().function_2_args(first_argument, second_argument=second_argument)
    TestClass.function_0_args()
