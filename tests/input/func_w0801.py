"""test code similarities
by default docstring are not considered
"""
__revision__ = 'id'
A = 2
B = 3
C = A + B
# need more than X lines to trigger the message
C *= 2
A -= B
# all this should be detected
