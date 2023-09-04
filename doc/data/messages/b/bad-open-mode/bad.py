def open_and_get_content(file_path):
    with open(file_path, "rwx") as file:  # [bad-open-mode]
        return file.read()
