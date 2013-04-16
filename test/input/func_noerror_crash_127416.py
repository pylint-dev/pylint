"""
FUNCTIONALITY
"""

class Example(object):
    """
      @summary: Demonstrates pylint error caused by method expecting tuple
      but called method does not return tuple
    """

    def method_expects_tuple(self, obj):
        m, args = self.method_doesnot_return_tuple(obj)
        result = m(args)
        return result

    def method_doesnot_return_tuple(self, obj):
        # we want to lock what we have in the inventory, not what is to have
        # in the future
        return {'success': ''}
