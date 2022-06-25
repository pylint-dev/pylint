username = "Ada"
code_to_execute = f"""input('Enter code to be executed please, {username}: ')"""
program = exec(code_to_execute)  # [exec-used]
exec(program)  # [exec-used]
