# pylint: disable=missing-docstring,consider-using-with,trailing-whitespace,unused-import

import os
import tempfile
import unittest
from pylint import lint
from pylint.testutils import GenericTestReporter

class ModuleShadowingTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.pkg_dir = os.path.join(self.tempdir.name, "my_module")
        os.makedirs(self.pkg_dir)
        
        with open(os.path.join(self.pkg_dir, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("")
        
        self.utils_file = os.path.join(self.pkg_dir, "utils.py")
        with open(self.utils_file, "w", encoding="utf-8") as f:
            f.write("def format():\n    pass\n\ndef other_method():\n    pass\n")
        
        self.test_file = os.path.join(self.tempdir.name, "main.py")

    def tearDown(self):
        self.tempdir.cleanup()

    def _run_pylint(self, code):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(code)
        
        reporter = GenericTestReporter()
        lint.Run(
            [
                "--disable=all",
                "--enable=no-name-in-module",
                "--persistent=no",
                "--rcfile=",
                self.test_file
            ],
            reporter=reporter,
            exit=False
        )
        return reporter.messages

    def test_shadowed_format_call(self):
        code = "import my_module.utils as my_module\nmy_module.format()\n"
        messages = self._run_pylint(code)
        errors = [msg for msg in messages if msg.msg_id == "E0611"]
        self.assertEqual(len(errors), 0)

    def test_shadowed_other_method(self):
        code = "import my_module.utils as my_module\nmy_module.other_method()\n"
        messages = self._run_pylint(code)
        errors = [msg for msg in messages if msg.msg_id == "E0611"]
        self.assertEqual(len(errors), 0)

    def test_non_shadowed_import(self):
        code = "import my_module.utils as utils\nutils.format()\n"
        messages = self._run_pylint(code)
        errors = [msg for msg in messages if msg.msg_id == "E0611"]
        self.assertEqual(len(errors), 0)

    def test_shadowed_import_without_call(self):
        code = "import my_module.utils as my_module\n"
        messages = self._run_pylint(code)
        errors = [msg for msg in messages if msg.msg_id == "E0611"]
        self.assertEqual(len(errors), 0)

if __name__ == "__main__":
    unittest.main()
