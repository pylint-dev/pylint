"""
Check accessing Exception.message
"""
# pylint: disable=import-error, no-absolute-import, broad-except

from unknown import ExtensionException
__revision__ = 0

class SubException(IndexError):
    """ empty """

_ = IndexError("test").message # [exception-message-attribute]
_ = ZeroDivisionError("error").message # [exception-message-attribute]
_ = ExtensionException("error").message
_ = SubException("error").message # [exception-message-attribute]

try:
    raise Exception('e')
except Exception as exception:
    _ = exception.message # [exception-message-attribute]
    del exception.message # [exception-message-attribute]
    exception.message += 'hello world' # [exception-message-attribute]
    exception.message = 'hello world'


class CompatException(Exception):
    """An exception which should work on py2 and py3."""

    def __init__(self, message=''):
        super(CompatException, self).__init__()
        self.message = message

    def __repr__(self):
        result = 'CompatException %s' % self.message
        return result.encode('utf-8')


try:
    raise CompatException('message here')
except CompatException as error:
    _ = error.message
