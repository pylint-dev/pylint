# https://github.com/PyCQA/pylint/issues/5801
# pylint: disable=missing-docstring

import struct
struct.unpack('h', b'\x00\x01')
