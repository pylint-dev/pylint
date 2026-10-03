# pylint: disable=missing-docstring,redefined-builtin,unsubscriptable-object
# pylint: disable=invalid-name,too-few-public-methods,attribute-defined-outside-init
class Repository:
    def _transfer(self, bytes=-1):
        self._bytesTransfered = 0
        bufff = True
        while bufff and (bytes < 0 or self._bytesTransfered < bytes):
            bufff = bufff[: bytes - self._bytesTransfered]
            self._bytesTransfered += len(bufff)
