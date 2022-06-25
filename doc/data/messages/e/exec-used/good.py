def get_user_code(username):
    return input(f'Enter code to be executed please, {username}: ')

username = "Ada"
globals = {'__builtins__' : None}
locals = {'print': print}
exec(get_user_code(username), globals, locals)  # pylint: disable=exec-used
