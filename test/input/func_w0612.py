"""test unused variable
"""

__revision__ = 0

def function(matches):
    """"yo"""
    aaaa = 1
    index = -1
    for match in matches:
        index += 1
        print match

def visit_if(self, node):
    """increments the branchs counter"""
    branchs = 1
    # don't double count If nodes coming from some 'elif'
    if node.orelse and len(node.orelse) > 1:
        branchs += 1
    self.inc_branch(branchs)
    self.stmts += branchs

