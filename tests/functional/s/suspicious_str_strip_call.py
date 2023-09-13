"""Suspicious str.strip calls."""
# pylint: disable=redundant-u-string-prefix


''.strip('yo')
''.strip()

u''.strip('http://')  # [bad-str-strip-call]
u''.lstrip('http://')  # [bad-str-strip-call]
b''.rstrip('http://')  # [bad-str-strip-call]
