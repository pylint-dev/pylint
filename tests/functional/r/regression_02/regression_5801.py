# https://github.com/pylint-dev/pylint/issues/5801
# pylint: disable=missing-docstring

import struct
struct.unpack('h', b'\x00\x01')
