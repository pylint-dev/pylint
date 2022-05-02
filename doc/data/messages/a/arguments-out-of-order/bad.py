def function_3_args(first_argument, second_argument, third_argument):
    """Three arguments function"""
    return first_argument, second_argument, third_argument


def args_out_of_order():
    first_argument = 1
    second_argument = 2
    third_argument = 3

    function_3_args(  # [arguments-out-of-order]
        first_argument, third_argument, second_argument
    )
