"""Check multiple key definition"""
# pylint: disable=pointless-statement, redundant-u-string-prefix

from enum import Enum


class MyEnum(Enum):
    """ Sample Enum for testing duplicate keys"""
    KEY = "key"



correct_dict = {
    'tea': 'for two',
    'two': 'for tea',
}

wrong_with_enum = {  # [duplicate-key]
    MyEnum.KEY: "value 1",
    MyEnum.KEY: "value 2",
}

wrong_dict = {  # [duplicate-key]
    'tea': 'for two',
    'two': 'for tea',
    'tea': 'time',

}

{1: b'a', 1: u'a'} # [duplicate-key]
{1: 1, 1.0: 2} # [duplicate-key]
