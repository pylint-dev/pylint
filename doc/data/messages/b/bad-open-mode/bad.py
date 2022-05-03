def foo(file_path):
    with open(file_path, "rwx") as file:  # [bad-open-mode]
        contents = file.read()
