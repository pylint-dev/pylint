"""Suspicious str.strip calls."""
# pylint: disable=redundant-u-string-prefix
__revision__ = 1

''.strip('yo')
''.strip()

u''.strip('http://')  # [bad-str-strip-call]
u''.lstrip('http://')  # [bad-str-strip-call]
b''.rstrip('http://')  # [bad-str-strip-call]
