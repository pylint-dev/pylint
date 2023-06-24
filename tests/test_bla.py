from pylint import testutils
from pylint.testutils.functional import FunctionalTestFile


def test_bla_1() -> None:
    __tracebackhide__ = True  # pylint: disable=unused-variable
    # pytestconfig = Config()
    pytestconfig = None
    test_file = FunctionalTestFile("tests", "bla_test.py")
    lint_test = testutils.LintModuleTest(test_file, pytestconfig)

    lint_test.setUp()
    lint_test.runTest()
