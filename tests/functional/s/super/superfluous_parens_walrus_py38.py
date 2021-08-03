"""Test the superfluous-parens warning with python 3.8 functionality (walrus operator)"""
# pylint: disable=missing-function-docstring,invalid-name
if not (x := False):
    print(x)

if not ((x := 1)):  # [superfluous-parens]
    pass

if not ((((x := 1)))):  # [superfluous-parens]
    pass

i = 1
y = 1

if odd := is_odd(i): # [undefined-variable]
    pass
if not (foo := 5):
    pass

if not ((x := y)):  # [superfluous-parens]
    pass

if ((x := y)):   # [superfluous-parens]
    pass

assert (ret := str(42))

# False positive (str, tuple)
A = [int(n) for n in (nums := '123')]
B = [int(n) for n in (nums := ('1', '2', '3'))]

# No false positive (list, set, dict)
C = [int(n) for n in (nums := ['1', '2', '3'])]
D = [int(n) for n in (nums := {'1', '2', '3'})]
E = [int(n) for n in (nums := {'1': 1, '2': 2, '3': 3})]

# False positive (brackets only)
F = [int(n) for n in (nums := ['1'])]
G = [int(n) for n in (nums := {'1'})]
H = [int(n) for n in (nums := {'1': 1})]
I = [int(n) for n in (nums := ('1'))]
J = [int(n) for n in (nums := ('1', ))]

# No false positive (brackets plus comma)
K = [int(n) for n in (nums := ['1', ])]
L = [int(n) for n in (nums := {'1', })]
M = [int(n) for n in (nums := {'1': 1, })]

# False positives (comma outside brackets)
N = [int(next(iter(n))) for n in (nums := (['1'], ['2'], ['3']))]
O = [int(next(iter(n))) for n in (nums := ({'1'}, {'2'}, {'3'}))]
P = [int(next(iter(n))) for n in (nums := ({'1': 1}, {'2': 2}, {'3': 3}))]

# False positives (aliasing)
NUMS_LIST = ['1', '2', '3']
NUMS_SET = {'1', '2', '3'}
NUMS_DICT = {'1': 1, '2': 2, '3': 3}
Q = [int(n) for n in (nums := NUMS_LIST)]
R = [int(n) for n in (nums := NUMS_SET)]
S = [int(n) for n in (nums := NUMS_DICT)]
T = [int(n) for n in (nums := [*NUMS_LIST])]
U = [int(n) for n in (nums := NUMS_LIST[:])]

# 2D arrays with numpy (since they allow commas within indexing)
import numpy
ARRAY_2D = numpy.zeroes((3, 3), dtype=bool)
V = not (vals := ARRAY_2D[:, :])  # No false positive
X = not (vals := ARRAY_2D[2, 2])  # No false positive
W = not (vals := ARRAY_2D[::])  # False positive
Y = not (vals := ARRAY_2D[2:2])  # False positive
Z = not (just_want_to_finish_the_alphabet := True)  # False positive

x = ("Version " + __version__) in output 
y = 2 + (5 * 3)
assert "Version " + __version__ in output
assert "" + ("Version " + __version__) in output
assert ("Version " + __version__) in output

class YieldRegression3249:
    @classmethod
    def from_json(cls, json):
        """Yields records from a JSON-ish dict."""
        modules = json.pop('modules', None) or ()
        yield (order := super().from_json(json))
        for module in modules:
            yield OrderedModule(order=order, module=Module(module))
            
            
