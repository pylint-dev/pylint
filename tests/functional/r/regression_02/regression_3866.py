# pylint: disable=missing-module-docstring, missing-docstring
# pylint: disable=invalid-name

# These trigger the bug
def lambda_with_args():
    variable = 1
    return lambda *_, variable=variable: variable + 1


def lambda_with_args_kwargs():
    variable = 1
    return lambda *_, variable=variable, **_kwargs: variable + 1


def lambda_with_args_and_multi_args():
    variable = 1
    return lambda *_, a, variable=variable: variable + a


# The rest of these do not trigger the bug
def lambda_with_multi_args():
    variable = 1
    return lambda a, variable=variable: variable + a


def lambda_without_args():
    variable = 1
    return lambda variable=variable: variable + 1


def lambda_with_kwargs():
    variable = 1
    return lambda variable=variable, **_: variable + 1


def func_def():
    variable = 1

    def f(*_, variable=variable):
        return variable + 1

    return f


def different_name():
    variable = 1
    return lambda *args, var=variable: var + 1
