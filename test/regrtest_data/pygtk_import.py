#pylint: disable=R0903,R0904
"""#10026"""
__revision__ = 1
from gtk import VBox
import gtk

class FooButton(gtk.Button):
    """extend gtk.Button"""
    def extend(self):
        """hop"""
        print self

print gtk.Button
print VBox
