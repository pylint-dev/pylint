# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the package-module-conflict check."""
import os

import astroid
from pylint import interfaces
from pylint.checkers import refactoring
from pylint.testutils import CheckerTestCase, Message


class TestCheckerModuleConflict(CheckerTestCase):

    CHECKER_CLASS = refactoring.RefactoringChecker

    def test_package_module_conflict(self):
        here = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(here, 'my_wrong_package', 'my_wrong_subpackage.py')
        with open(path) as stream:
            data = stream.read()
        module = astroid.parse(data, module_name='my_wrong_subpackage',
                               path=path)
        args = ('../../my_wrong_package/my_wrong_subpackage',
                '../../my_wrong_package/my_wrong_subpackage.py')
        msg = Message(msg_id='package-module-conflict', node=module, args=args,
                      confidence=interfaces.UNDEFINED)
        with self.assertAddsMessages(msg):
            self.checker.visit_module(module)
