from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker

class MyASTNGChecker(BaseChecker):
    """add member attributes defined using my own "properties" function
    to the class locals dictionary
    """
    
    __implements__ = IASTNGChecker

    name = 'custom'
    msgs = {}
    options = ()
    # this is important so that your checker is executed before others
    priority = -1 

    def visit_callfunc(self, node):
        """called when a CallFunc node is encountered.

        See logilab.astng for the description of available nodes."""
        if not (isinstance(node.func, astng.Getattr)
                and isinstance(node.func.expr, astng.Name)
                and node.func.expr.name == 'properties'
                and node.func.attrname == 'create'):
            return
        in_class = node.frame()
        for param in node.args:
            in_class.locals[param.name] = node

    
def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(MyASTNGChecker(linter))
        
