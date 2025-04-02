def get_user_code(name):
    return input(f"Enter code to be executed please, {name}: ")


username = "Ada"
# If the globals dictionary does not contain a value for the key __builtins__,
# all builtins are allowed. You need to be explicit about it being disallowed.
allowed_globals = {"__builtins__": {}}
allowed_locals = {}
# pylint: disable-next=exec-used
exec(get_user_code(username), allowed_globals, allowed_locals)
