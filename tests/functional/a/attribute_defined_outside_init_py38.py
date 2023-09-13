# pylint: disable=missing-docstring

import unittest


class AsyncioTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.i = 42
