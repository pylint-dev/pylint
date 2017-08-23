.. _ide-integration:

###########################
 Editor and IDE integration
###########################

To use Pylint with:

 - Emacs_, see http://www.emacswiki.org/emacs/PythonProgrammingInEmacs#toc8,
 - Vim_, see http://www.vim.org/scripts/script.php?script_id=891,
 - `Visual Studio`_, see https://docs.microsoft.com/visualstudio/python/code-pylint,
 - Eclipse_ and PyDev_, see http://pydev.org/manual_adv_pylint.html,
 - Komodo_, see http://mateusz.loskot.net/posts/2006/01/15/running-pylint-from-komodo/,
 - gedit_, see https://launchpad.net/gedit-pylint-2 or https://wiki.gnome.org/Apps/Gedit/PylintPlugin,
 - WingIDE_, see http://www.wingware.com/doc/edit/pylint,
 - PyCharm_, see :ref:`the section below <pylint_in_pycharm>`,
 - TextMate_, see :ref:`the section below <pylint_in_textmate>`

Pylint is integrated in:

 - `Visual Studio`_, see the `Python > Run PyLint` command on a project's context menu.
 - Eric_ IDE, see the `Project > Check` menu,
 - Spyder_, see http://packages.python.org/spyder/pylint.html,
 - pyscripter_, see the `Tool -> Tools` menu.

.. _Emacs: http://www.gnu.org/software/emacs/
.. _Vim: http://www.vim.org/
.. _Visual Studio: https://www.visualstudio.com/
.. _Eclipse: https://www.eclipse.org/
.. _Eric: http://eric-ide.python-projects.org/
.. _pyscripter: http://code.google.com/p/pyscripter/
.. _pydev: http://pydev.org
.. _Komodo: http://www.activestate.com/Products/Komodo/
.. _gedit: https://wiki.gnome.org/Apps/Gedit
.. _WingIDE: http://www.wingware.com/
.. _spyder: http://code.google.com/p/spyderlib/
.. _PyCharm: http://www.jetbrains.com/pycharm/
.. _TextMate: http://macromates.com

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
