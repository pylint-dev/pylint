"""Import PyGTK."""
#pylint: disable=too-few-public-methods,too-many-public-methods

from gtk import VBox
import gtk

class FooButton(gtk.Button):
    """extend gtk.Button"""
    def extend(self):
        """hop"""
        print self

print gtk.Button
print VBox
