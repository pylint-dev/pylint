import os

EXTENSIONS_DIRECTORY = "pylint/extensions"
extension_names = [
    filename
    for filename in os.listdir(EXTENSIONS_DIRECTORY)
    if filename.endswith(".py") and not filename.startswith("_")
]
