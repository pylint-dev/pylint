class TreeNode(object):
    """ Class containing variables to be used in a Binary Search Tree """
    def __init__(self, xVal):
        self.val = xVal
        self.left = None
        self.right = None

def closestValue(root, target):
    """ Function used to fing the closest value of a given target value in a given
        non-empty Binary Search Tree (BST) of unique values """
    aVal = root.val
    kid = root.left if target < aVal else root.right
    if not kid:
        return aVal
    bVal = closestValue(kid, target)

    return min((aVal, bVal), key=lambda x: abs(target-x))

root = TreeNode(8)
root.left = TreeNode(5)
root.right = TreeNode(14)
root.left.left = TreeNode(4)
root.left.right = TreeNode(6)
root.left.right.left = TreeNode(8)
root.left.right.right = TreeNode(7)
root.right.right = TreeNode(24)
root.right.right.left = TreeNode(22)

result = closestValue(root, 19)
print(result)
