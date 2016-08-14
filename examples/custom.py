import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker

class MyAstroidChecker(BaseChecker):
    """add member attributes defined using my own "properties" function
    to the class locals dictionary
    """
    
    __implements__ = IAstroidChecker

    name = 'custom'
    msgs = {
        'W0001': ('Message that will be emitted',
                  'message-symbol',
                  'Message help')
    }
    options = ()
    # this is important so that your checker is executed before others
    priority = -1 

    def visit_callfunc(self, node):
        """called when a CallFunc node is encountered.

        See astroid for the description of available nodes."""
        if not (isinstance(node.func, astroid.Getattr)
                and isinstance(node.func.expr, astroid.Name)
                and node.func.expr.name == 'properties'
                and node.func.attrname == 'create'):
            return
        in_class = node.frame()
        for param in node.args:
            in_class.locals[param.name] = node

    
def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(MyAstroidChecker(linter))
        
