# pylint: disable=missing-docstring
from toml import TomlEncoder
from yaml import YAMLObject

class Control: # [too-few-public-methods]
    ...


class MyTomlEncoder(TomlEncoder):
    ...


class MyYAMLObject(YAMLObject):
    ...
