def get_user_code(name):
    return input(f"Enter code to be executed please, {name}: ")


username = "Ada"
allowed_globals = {"__builtins__": None}
allowed_locals = {"print": print}
# pylint: disable-next=exec-used
exec(get_user_code(username), allowed_globals, allowed_locals)
