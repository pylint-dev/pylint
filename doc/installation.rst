Installation
------------


Python packages
'''''''''''''''

Pylint should be easily installable using pip.

.. code-block:: sh

   python -m pip install pip


Source distribution installation
''''''''''''''''''''''''''''''''

From the source distribution, extract the tarball, go to the extracted
directory and simply run ::

    python setup.py install

Or you can install it in editable mode, using ::

    python setup.py develop


Note for Windows users
''''''''''''''''''''''

On Windows, once you have installed Pylint, the command line usage is ::

  pylint.bat [options] module_or_package

But this will only work if *pylint.bat* is either in the current
directory, or on your system path. (*setup.py* will install *python.bat*
to the *Scripts* subdirectory of your Python installation -- e.g.
C:\Python24\Scripts.) You can do any of the following to solve this:

1. Change to the appropriate directory before running pylint.bat

2. Add the Scripts directory to your path statement in your autoexec.bat
   file (this file is found in the root directory of your boot-drive)

3. Create a 'redirect' batch file in a directory actually on your
   systems path

To effect (2), simply append the appropriate directory name to the PATH=
statement in autoexec.bat. Be sure to use the Windows directory
separator of ';' between entries. Then, once you have rebooted (this is
necessary so that the new path statement will take effect when
autoexec.bat is run), you will be able to invoke Pylint with
pylint.bat on the command line.

(3) is the best solution. Once done, you can call Pylint at the command
line without the .bat, just as do non-Windows users by typing: ::

  pylint [options] module_or_package

To effect option (3), simply create a plain text file pylint.bat with
the single line: ::

  C:\PythonDirectory\Scripts\pylint.bat

(where PythonDirectory is replaced by the actual Python installation
directory on your system -- e.g. C:\Python24\Scripts\pylint.bat).

Alternatively, you can run pylint using the ``-m`` flag, as in:

.. code-block:: sh

    python -m pylint module_or_package
