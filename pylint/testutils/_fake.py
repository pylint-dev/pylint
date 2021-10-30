# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""This file is intended to only be used for testing namespace package importing.

   Importing a file has a global side effect of adding a module to sys.modules.
   As namespace packages are sensitive to sys.path, to test them we check
   an intentional import error and a successful import. To avoid the imports
   messing up the test environment, we need to make the import error use
   a file that is never imported by any other test. This serves as that file.
"""
