.. _pylint_in_flymake:

Using Pylint through Flymake in Emacs
=====================================

.. warning::
   The Emacs package now has its own repository and is looking for a maintainer.
   If you're reading this doc and are interested in maintaining this package or
   are actually using flymake please open an issue at
   https://github.com/emacsorphanage/pylint/issues/new/choose

To enable Flymake for Python, insert the following into your .emacs:

.. sourcecode:: common-lisp

    ;; Configure Flymake for Python
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


Finally, by default Flymake only displays the extra information about the error when you
hover the mouse over the highlighted line. The following will use the minibuffer to display
messages when you the cursor is on the line.

.. sourcecode:: common-lisp

    ;; To avoid having to mouse hover for the error message, these functions make Flymake error messages
    ;; appear in the minibuffer
    (defun show-fly-err-at-point ()
      "If the cursor is sitting on a Flymake error, display the message in the minibuffer"
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
