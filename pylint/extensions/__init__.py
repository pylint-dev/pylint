import os

EXTENSIONS_DIRECTORY = os.path.dirname(__file__)
extension_names = [
    filename
    for filename in os.listdir(EXTENSIONS_DIRECTORY)
    if filename.endswith(".py") and not filename.startswith("_")
]
