Integrate Pylint with PyCharm
=============================

.. _pylint_in_pycharm:

Install Pylint the usual way::

    pip install pylint

Remember the path at which it's installed::

    which pylint

Using pylint-pycharm plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#.  In PyCharm go to *Preferences* > *Plugins* > *Browse repositories...*
#.  Right-click on the plugin named **Pylint**, select **Download and Install** and restart PyCharm when prompted

If the plugin is not finding the Pylint executable (e.g. is not inside the PATH environmental variable), you can
specify it manually using the plugin settings:

#.  *Preferences* > *Other Settings* > *Pylint* or simply click the gear icon from the side bar of the Pylint tool window
#.  Type the path directly or use the Browse button to open a file selection dialog
#.  Press the Test button to check if the plugin is able to run the executable

For more info on how to use the plugin please check the `official plugin documentation <https://github.com/leinardi/pylint-pycharm/blob/master/README.md>`_.

Using External Tools
~~~~~~~~~~~~~~~~~~~~

Within PyCharm:

#.  Navigate to the preferences window
#.  Select "External Tools"
#.  Click the plus sign at the bottom of the dialog to add a new external task
#.  In the dialog, populate the following fields:

    :Name:                              Pylint
    :Description:                       A Python source code analyzer which looks for programming errors, helps enforcing a coding standard and sniffs for some code smells.
    :Synchronize files after execution: unchecked
    :Program:                           ``/path/to/pylint``
    :Parameters:                        ``$FilePath$``

#.  Click OK

The option to check the current file with Pylint should now be available in *Tools* > *External Tools* > *Pylint*.
