class SomeException(Exception):
    pass


AliasException = SomeException

try:
    pass
except Exception:
    pass


try:
    pass
except SomeException:
    pass


try:
    pass
except AliasException:
    pass
