def open_and_get_content(file_path):
    with open(file_path, "r") as file:
        return file.read()
