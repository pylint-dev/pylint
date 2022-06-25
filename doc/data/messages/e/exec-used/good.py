def get_user_code(username):
    return input(f'Enter code to be executed please, {username}: ')

username = "Ada"
exec(get_user_code(username))  # pylint: disable=exec-used
