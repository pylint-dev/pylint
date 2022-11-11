def get_user_code(name):
    return input(f'Enter code to be executed please, {name}: ')


username = "Ada"
allowed_globals = {'__builtins__' : None}
allowed_locals = {'print': print}
exec(get_user_code(username), allowed_globals, allowed_locals)  # pylint: disable=exec-used
