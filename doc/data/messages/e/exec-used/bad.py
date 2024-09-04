def get_user_code(name):
    return input(f"Enter code to be executed please, {name}: ")


exec(get_user_code("Ada"))  # [exec-used]
