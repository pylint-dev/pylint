;;; pylint.el --- minor mode for running `pylint'

;; Copyright (c) 2009, 2010 Ian Eure <ian.eure@gmail.com>
;; Author: Ian Eure <ian.eure@gmail.com>
;; Maintainer: Jonathan Kotta <jpkotta@gmail.com>

;; Keywords: languages python
;; Version: 1.02

;; pylint.el is free software; you can redistribute it and/or modify it
;; under the terms of the GNU General Public License as published by the Free
;; Software Foundation; either version 2, or (at your option) any later
;; version.
;;
;; It is distributed in the hope that it will be useful, but WITHOUT ANY
;; WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
;; FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
;; details.
;;
;; You should have received a copy of the GNU General Public License along
;; with your copy of Emacs; see the file COPYING.  If not, write to the Free
;; Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
;; MA 02110-1301, USA

;;; Commentary:
;;
;; Specialized compile mode for pylint.  You may want to add the
;; following to your init.el:
;;
;;   (autoload 'pylint "pylint")
;;   (add-hook 'python-mode-hook 'pylint-add-menu-items)
;;   (add-hook 'python-mode-hook 'pylint-add-key-bindings)
;;
;; There is also a handy command `pylint-insert-ignore-comment' that
;; makes it easy to insert comments of the form `# pylint:
;; ignore=msg1,msg2,...'.

;;; Code:

(require 'compile)
(require 'tramp)

(defgroup pylint nil
  "Minor mode for running the Pylint Python checker"
  :prefix "pylint-"
  :group 'tools
  :group 'languages)

(defvar pylint-last-buffer nil
  "The most recent PYLINT buffer.
A PYLINT buffer becomes most recent when you select PYLINT mode in it.
Notice that using \\[next-error] or \\[compile-goto-error] modifies
`completion-last-buffer' rather than `pylint-last-buffer'.")

(defconst pylint-regexp-alist
  (let ((base "^\\(.*\\):\\([0-9]+\\):\s+\\(\\[%s.*\\)$"))
    (list
     (list (format base "[FE]") 1 2)
     (list (format base "[RWC]") 1 2 nil 1)))
  "Regexp used to match PYLINT hits.  See `compilation-error-regexp-alist'.")

(defcustom pylint-options '("--reports=n" "--output-format=parseable")
  "Options to pass to pylint.py"
  :type '(repeat string)
  :group 'pylint)

(defcustom pylint-use-python-indent-offset nil
  "If non-nil, use `python-indent-offset' to set indent-string."
  :type 'boolean
  :group 'pylint)

(defcustom pylint-command "pylint"
  "PYLINT command."
  :type '(file)
  :group 'pylint)

(defcustom pylint-alternate-pylint-command "pylint2"
  "Command for pylint when invoked with C-u."
  :type '(file)
  :group 'pylint)

(defcustom pylint-ask-about-save nil
  "Non-nil means \\[pylint] asks which buffers to save before compiling.
Otherwise, it saves all modified buffers without asking."
  :type 'boolean
  :group 'pylint)

(defvar pylint--messages-list ()
  "A list of strings of all pylint messages.")

(defvar pylint--messages-list-hist ()
  "Completion history for `pylint--messages-list'.")

(defun pylint--sort-messages (a b)
  "Compare function for sorting `pylint--messages-list'.

Sorts most recently used elements first using `pylint--messages-list-hist'."
  (let ((idx 0)
        (a-idx most-positive-fixnum)
        (b-idx most-positive-fixnum))
    (dolist (e pylint--messages-list-hist)
      (when (string= e a)
        (setq a-idx idx))
      (when (string= e b)
        (setq b-idx idx))
      (setq idx (1+ idx)))
    (< a-idx b-idx)))

(defun pylint--create-messages-list ()
  "Use `pylint-command' to populate `pylint--messages-list'."
  ;; example output:
  ;;  |--we want this--|
  ;;  v                v
  ;; :using-cmp-argument (W1640): *Using the cmp argument for list.sort / sorted*
  ;;   Using the cmp argument for list.sort or the sorted builtin should be avoided,
  ;;   since it was removed in Python 3. Using either `key` or `functools.cmp_to_key`
  ;;   should be preferred. This message can't be emitted when using Python >= 3.0.
  (setq pylint--messages-list
        (split-string
         (with-temp-buffer
           (shell-command (concat pylint-command " --list-msgs") (current-buffer))
           (flush-lines "^[^:]")
           (goto-char (point-min))
           (while (not (eobp))
             (delete-char 1) ;; delete ";"
             (re-search-forward " ")
             (delete-region (point) (line-end-position))
             (forward-line 1))
           (buffer-substring-no-properties (point-min) (point-max))))))

;;;###autoload
(defun pylint-insert-ignore-comment (&optional arg)
  "Insert a comment like \"# pylint: disable=msg1,msg2,...\".

This command repeatedly uses `completing-read' to match known
messages, and ultimately inserts a comma-separated list of all
the selected messages.

With prefix argument, only insert a comma-separated list (for
appending to an existing list)."
  (interactive "*P")
  (unless pylint--messages-list
    (pylint--create-messages-list))
  (setq pylint--messages-list
        (sort pylint--messages-list #'pylint--sort-messages))
  (let ((msgs ())
        (msg "")
        (prefix (if arg
                    ","
                  "# pylint: disable="))
        (sentinel "[DONE]"))
    (while (progn
             (setq msg (completing-read
                        "Message: "
                        pylint--messages-list
                        nil t nil 'pylint--messages-list-hist sentinel))
             (unless (string= sentinel msg)
               (add-to-list 'msgs msg 'append))))
    (setq pylint--messages-list-hist
          (delete sentinel pylint--messages-list-hist))
    (insert prefix (mapconcat 'identity msgs ","))))

(define-compilation-mode pylint-mode "PYLINT"
  (setq pylint-last-buffer (current-buffer))
  (set (make-local-variable 'compilation-error-regexp-alist)
       pylint-regexp-alist)
  (set (make-local-variable 'compilation-disable-input) t))

(defvar pylint-mode-map
  (let ((map (make-sparse-keymap)))
    (set-keymap-parent map compilation-minor-mode-map)
    (define-key map " " 'scroll-up)
    (define-key map "\^?" 'scroll-down)
    (define-key map "\C-c\C-f" 'next-error-follow-minor-mode)

    (define-key map "\r" 'compile-goto-error)  ;; ?
    (define-key map "n" 'next-error-no-select)
    (define-key map "p" 'previous-error-no-select)
    (define-key map "{" 'compilation-previous-file)
    (define-key map "}" 'compilation-next-file)
    (define-key map "\t" 'compilation-next-error)
    (define-key map [backtab] 'compilation-previous-error)
    map)
  "Keymap for PYLINT buffers.
`compilation-minor-mode-map' is a cdr of this.")

(defun pylint--make-indent-string ()
  "Make a string for the `--indent-string' option."
  (format "--indent-string='%s'"
          (make-string python-indent-offset ?\ )))

;;;###autoload
(defun pylint (&optional arg)
  "Run PYLINT, and collect output in a buffer, much like `compile'.

While pylint runs asynchronously, you can use \\[next-error] (M-x next-error),
or \\<pylint-mode-map>\\[compile-goto-error] in the grep \
output buffer, to go to the lines where pylint found matches.

\\{pylint-mode-map}"
  (interactive "P")

  (save-some-buffers (not pylint-ask-about-save) nil)
  (let* ((filename (buffer-file-name))
         (filename (or (and (tramp-tramp-file-p filename)
                         (aref (tramp-dissect-file-name filename) 3))
                      filename))
         (filename (shell-quote-argument filename))
         (pylint-command (if arg
                             pylint-alternate-pylint-command
                           pylint-command))
         (pylint-options (if (not pylint-use-python-indent-offset)
                             pylint-options
                           (append pylint-options
                                   (list (pylint--make-indent-string)))))
         (command (mapconcat
                   'identity
                   (append `(,pylint-command) pylint-options `(,filename))
                   " ")))

    (compilation-start command 'pylint-mode)))

;;;###autoload
(defun pylint-add-key-bindings ()
  (let ((map (cond
              ((boundp 'py-mode-map) py-mode-map)
              ((boundp 'python-mode-map) python-mode-map))))

    ;; shortcuts in the tradition of python-mode and ropemacs
    (define-key map (kbd "C-c m l") 'pylint)
    (define-key map (kbd "C-c m p") 'previous-error)
    (define-key map (kbd "C-c m n") 'next-error)
    (define-key map (kbd "C-c m i") 'pylint-insert-ignore-comment)
    nil))

;;;###autoload
(defun pylint-add-menu-items ()
  (let ((map (cond
              ((boundp 'py-mode-map) py-mode-map)
              ((boundp 'python-mode-map) python-mode-map))))
  
    (define-key map [menu-bar Python pylint-separator]
      '("--" . pylint-separator))
    (define-key map [menu-bar Python next-error]
      '("Next error" . next-error))
    (define-key map [menu-bar Python prev-error]
      '("Previous error" . previous-error))
    (define-key map [menu-bar Python lint]
      '("Pylint" . pylint))
    nil))

(provide 'pylint)

;;; pylint.el ends here
