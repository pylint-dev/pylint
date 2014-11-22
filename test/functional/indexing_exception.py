"""
Check for indexing exceptions.
"""
# pylint: disable=import-error, no-absolute-import
__revision__ = 0

from unknown import ExtensionException

class SubException(IndexError):
    """ empty """

_ = IndexError("test")[0] # [indexing-exception]
_ = ZeroDivisionError("error")[0] # [indexing-exception]
_ = ExtensionException("error")[0]
_ = SubException("error")[1] # [indexing-exception]
