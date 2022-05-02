def foo(file_path):
    with open(file_path) as file:  # [unspecified-encoding]
        contents = file.read()
