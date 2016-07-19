# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the config module."""

import re
import sre_constants
import unittest

from pylint import config

class ConfigValidatorTest(unittest.TestCase):
    def test__regexp_validator_valid(self):
        result = config._regexp_validator(None, None, "test_.*")
        self.assertTrue(isinstance(result, re._pattern_type))
        self.assertEqual(result.pattern, "test_.*")

    def test__regexp_validator_invalid(self):
        with self.assertRaises(sre_constants.error):
            config._regexp_validator(None, None, "test_)")

    def test__csv_validator_no_spaces(self):
        values = ["One", "Two", "Three"]
        result = config._csv_validator(None, None, ",".join(values))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 3)
        for i, value in enumerate(values):
            self.assertEqual(result[i], value)

    def test__csv_validator_spaces(self):
        values = ["One", "Two", "Three"]
        result = config._csv_validator(None, None, ", ".join(values))
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 3)
        for i, value in enumerate(values):
            self.assertEqual(result[i], value)

    def test__regexp_csv_validator_valid(self):
        pattern_strings = ["test_.*", "foo\.bar", "^baz$"]
        result = config._regexp_csv_validator(None, None, ",".join(pattern_strings))
        for i, regex in enumerate(result):
            self.assertTrue(isinstance(regex, re._pattern_type))
            self.assertEqual(regex.pattern, pattern_strings[i])

    def test__regexp_csv_validator_invalid(self):
        pattern_strings = ["test_.*", "foo\.bar", "^baz)$"]
        with self.assertRaises(sre_constants.error):
            config._regexp_csv_validator(None, None, ",".join(pattern_strings))

if __name__ == "__main__":
    unittest.main()
