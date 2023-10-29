from configparser import ParsingError

err = ParsingError("filename")
source = err.filename  # [deprecated-attribute]
