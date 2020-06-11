.. _ide-integration:

###########################
 Editor and IDE integration
###########################

To use Pylint with:

 - Emacs_, see https://www.emacswiki.org/emacs/PythonProgrammingInEmacs#toc8,
 - Vim_, see https://www.vim.org/scripts/script.php?script_id=891,
 - `Visual Studio`_, see https://docs.microsoft.com/visualstudio/python/code-pylint,
 - Eclipse_ and PyDev_, see https://pydev.org/manual_adv_pylint.html,
 - Komodo_, see http://mateusz.loskot.net/posts/2006/01/15/running-pylint-from-komodo/,
 - gedit_, see https://launchpad.net/gedit-pylint-2 or https://wiki.gnome.org/Apps/Gedit/PylintPlugin,
 - WingIDE_, see https://www.wingware.com/doc/edit/pylint,
 - PyCharm_, see :ref:`the section below <pylint_in_pycharm>`,
 - TextMate_, see :ref:`the section below <pylint_in_textmate>`
 - `Visual Studio Code`_, see https://code.visualstudio.com/docs/python/linting#_pylint,

Pylint is integrated in:

 - `Visual Studio`_, see the `Python > Run PyLint` command on a project's context menu.
 - Eric_ IDE, see the `Project > Check` menu,
 - Spyder_, see the `View -> Panes -> Static code analysis` pane and
   its `corresponding documentation <https://docs.spyder-ide.org/pylint.html>`_.
 - pyscripter_, see the `Tool -> Tools` menu.
 - `Visual Studio Code`_, see the `Preferences -> Settings` menu.

.. _Emacs: https://www.gnu.org/software/emacs/
.. _Vim: https://www.vim.org/
.. _Visual Studio: https://www.visualstudio.com/
.. _Eclipse: https://www.eclipse.org/
.. _Eric: https://eric-ide.python-projects.org/
.. _pyscripter: https://github.com/pyscripter/pyscripter
.. _pydev: https://pydev.org
.. _Komodo: http://www.activestate.com/Products/Komodo/
.. _gedit: https://wiki.gnome.org/Apps/Gedit
.. _WingIDE: https://www.wingware.com/
.. _spyder: https://www.spyder-ide.org/
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _TextMate: https://macromates.com
.. _Visual Studio Code: https://code.visualstudio.com/

Using Pylint thru flymake in Emacs
==================================

To enable flymake for Python, insert the following into your .emacs:

.. sourcecode:: common-lisp

    ;; Configure flymake for Python
    (when (load "flymake" t)
      (defun flymake-pylint-init ()
        (let* ((temp-file (flymake-init-create-temp-buffer-copy
                           'flymake-create-temp-inplace))
               (local-file (file-relative-name
                            temp-file
                            (file-name-directory buffer-file-name))))
          (list "epylint" (list local-file))))
      (add-to-list 'flymake-allowed-file-name-masks
                   '("\\.py\\'" flymake-pylint-init)))

    ;; Set as a minor mode for Python
    (add-hook 'python-mode-hook '(lambda () (flymake-mode)))

Above stuff is in ``pylint/elisp/pylint-flymake.el``, which should be automatically
installed on Debian systems, in which cases you don't have to put it in your ``.emacs`` file.

Other things you may find useful to set:

.. sourcecode:: common-lisp

    ;; Configure to wait a bit longer after edits before starting
    (setq-default flymake-no-changes-timeout '3)

    ;; Keymaps to navigate to the errors
    (add-hook 'python-mode-hook '(lambda () (define-key python-mode-map "\C-cn" 'flymake-goto-next-error)))
    (add-hook 'python-mode-hook '(lambda () (define-key python-mode-map "\C-cp" 'flymake-goto-prev-error)))


Finally, by default flymake only displays the extra information about the error when you
hover the mouse over the highlighted line. The following will use the minibuffer to display
messages when you the cursor is on the line.

.. sourcecode:: common-lisp

    ;; To avoid having to mouse hover for the error message, these functions make flymake error messages
    ;; appear in the minibuffer
    (defun show-fly-err-at-point ()
      "If the cursor is sitting on a flymake error, display the message in the minibuffer"
      (require 'cl)
      (interactive)
      (let ((line-no (line-number-at-pos)))
        (dolist (elem flymake-err-info)
          (if (eq (car elem) line-no)
    	  (let ((err (car (second elem))))
    	    (message "%s" (flymake-ler-text err)))))))

    (add-hook 'post-command-hook 'show-fly-err-at-point)


Alternative, if you only wish to pollute the minibuffer after an explicit flymake-goto-* then use
the following instead of a post-command-hook

.. sourcecode:: common-lisp

    (defadvice flymake-goto-next-error (after display-message activate compile)
      "Display the error in the mini-buffer rather than having to mouse over it"
      (show-fly-err-at-point))

    (defadvice flymake-goto-prev-error (after display-message activate compile)
      "Display the error in the mini-buffer rather than having to mouse over it"
      (show-fly-err-at-point))

.. _pylint_in_pycharm:

Integrate Pylint with PyCharm
=============================

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


.. _pylint_in_textmate:

Integrate Pylint with TextMate
==============================

Install Pylint in the usual way::

    pip install pylint

Install the `Python bundle for TextMate <https://github.com/textmate/python.tmbundle>`_:

#.  select *TextMate* > *Preferences*
#.  select the *Bundles* tab
#.  find and tick the *Python* bundle in the list

You should now see it in *Bundles* > *Python*.

In *Preferences*, select the *Variables* tab. If a ``TM_PYCHECKER`` variable is not already listed, add
it, with the value ``pylint``.

The default keyboard shortcut to run the syntax checker is *Control-Shift-V* - open a ``.py`` file
in Textmate, and try it.

You should see the output in a new window:

    PyCheckMate 1.2 – Pylint 1.4.4

    No config file found, using default configuration

Then all is well, and most likely Pylint will have expressed some opinions about your Python code
(or will exit with ``0`` if your code already conforms to its expectations).

If you receive a message:

    Please install PyChecker, PyFlakes, Pylint, PEP 8 or flake8 for more extensive code checking.

That means that Pylint wasn't found, which is likely an issue with command paths - TextMate needs
be looking for Pylint on the right paths.

Check where Pylint has been installed, using ``which``::

    $ which pylint
    /usr/local/bin/pylint

The output will tell you where Pylint can be found; in this case, in ``/usr/local/bin``.

#. select *TextMate* > *Preferences*
#. select the *Variables* tab
#. find and check that a ``PATH`` variable exists, and that it contains the appropriate path (if
   the path to Pylint were ``/usr/local/bin/pylint`` as above, then the variable would need to
   contain ``/usr/local/bin``). An actual example in this case might be
   ``$PATH:/opt/local/bin:/usr/local/bin:/usr/texbin``, which includes other paths.

... and try running Pylint again.

Integrate Pylint with Visual Studio Code
========================================

Command-line arguments and configuration files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `Pylint command line arguments`_ for general switches. Command line
arguments can be used to load Pylint plugins, such as that for Django:

::

    "python.linting.pylintArgs": ["--load-plugins", "pylint_django"]

Options can also be specified in a ``pylintrc`` or ``.pylintrc`` file in
the workspace folder, as described on `Pylint command line arguments`_.

To control which Pylint messages are shown, add the following contents
to an options file:

.. code:: ini

    [MESSAGES CONTROL]

    # Enable the message, report, category or checker with the given id(s). You can
    # either give multiple identifier separated by comma (,) or put this option
    # multiple time.
    #enable=

    # Disable the message, report, category or checker with the given id(s). You
    # can either give multiple identifier separated by comma (,) or put this option
    # multiple time (only on the command line, not in the configuration file where
    # it should appear only once).
    #disable=

Message category mapping
~~~~~~~~~~~~~~~~~~~~~~~~

The Python extension maps Pylint message categories to VS Code
categories through the following settings. If desired, change the
setting to change the mapping.

+----------------------+-----------------------------------+------------------+
| Pylint category      | Applicable setting                | VS Code category |
|                      | (python.linting.)                 | mapping          |
+======================+===================================+==================+
| convention           | pylintCategorySeverity.convention | Information      |
+----------------------+-----------------------------------+------------------+
| refactor             | pylintCategorySeverity.refactor   | Hint             |
+----------------------+-----------------------------------+------------------+
| warning              | pylintCategorySeverity.warning    | Warning          |
+----------------------+-----------------------------------+------------------+
| error                | pylintCategorySeverity.error      | Error            |
+----------------------+-----------------------------------+------------------+
| fatal                | pylintCategorySeverity.fatal      | Error            |
+----------------------+-----------------------------------+------------------+

.. _Pylint command line arguments: https://pylint.readthedocs.io/en/latest/user_guide/run.html#command-line-options
