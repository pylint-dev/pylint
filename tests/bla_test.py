"""module docstring"""


def a_function(test_var):
    """func docstring"""
    if test_var == 2:
        if test_var:
            possibly_undefined_var = 1
        else:
            possibly_undefined_var = 2
    return possibly_undefined_var


# TODO: doesn't detect this?
# def a_function(test_var):
#     """func docstring"""
#     if test_var == 2:
#         if test_var:
#             possibly_undefined_var = 1
#         else:
#             possibly_undefined_var = 2
#         return possibly_undefined_var
#     return possibly_undefined_var
