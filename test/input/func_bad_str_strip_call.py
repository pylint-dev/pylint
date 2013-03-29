"""Suspicious str.strip calls."""
__revision__ = 1

''.strip('yo')
''.strip()

u''.strip('http://')
u''.lstrip('http://')
b''.rstrip('http://')
