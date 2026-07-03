from pylint.checkers.exceptions import ExceptionsChecker
from pylint.checkers.stdlib import StdlibChecker
from pylint.extensions.check_elif import ElseifUsedChecker


class CheckerCollector:
    def __init__(self):
        self.checker1 = ExceptionsChecker(None)
        self.checker2 = ElseifUsedChecker(None)
        self.checker3 = StdlibChecker(None)
