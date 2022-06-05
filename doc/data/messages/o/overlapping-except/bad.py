class SomeException(Exception):
    pass


AliasException = SomeException

try:
    pass
except (Exception, SomeException):  # [overlapping-except]
    pass


try:
    pass
except (SomeException, SomeException):  # [overlapping-except]
    pass


try:
    pass
except (AliasException, SomeException):  # [overlapping-except]
    pass
