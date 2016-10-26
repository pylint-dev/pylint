"""
Check accessing Exception.message
"""
# pylint: disable=import-error, no-absolute-import

from unknown import ExtensionException
__revision__ = 0

class SubException(IndexError):
    """ empty """

_ = IndexError("test").message # [exception-message-attribute]
_ = ZeroDivisionError("error").message # [exception-message-attribute]
_ = ExtensionException("error").message
_ = SubException("error").message # [exception-message-attribute]
