;;; pylint.el --- minor mode for running `pylint'

;; Copyright (c) 2009, 2010 Ian Eure <ian.eure@gmail.com>

;; Author: Ian Eure <ian.eure@gmail.com>

;; Keywords: languages python
;; Version: 1.01

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
`complation-last-buffer' rather than `pylint-last-buffer'.")

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

(defcustom pylint-command "pylint"
  "PYLINT command."
  :type '(file)
  :group 'pylint)

(defcustom pylint-ask-about-save nil
  "Non-nil means \\[pylint] asks which buffers to save before compiling.
Otherwise, it saves all modified buffers without asking."
  :type 'boolean
  :group 'pylint)

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

;;;###autoload
(defun pylint ()
  "Run PYLINT, and collect output in a buffer, much like `compile'.

While pylint runs asynchronously, you can use \\[next-error] (M-x next-error),
or \\<pylint-mode-map>\\[compile-goto-error] in the grep \
output buffer, to go to the lines where pylint found matches.

\\{pylint-mode-map}"
  (interactive)

  (save-some-buffers (not pylint-ask-about-save) nil)
  (let* ((tramp (tramp-tramp-file-p (buffer-file-name)))
         (file (or (and tramp
                        (aref (tramp-dissect-file-name (buffer-file-name)) 3))
                   (buffer-file-name)))
         (command (mapconcat
                   'identity
                   (list pylint-command
                         (mapconcat 'identity pylint-options " ")
                         (shell-quote-argument file)) " ")))

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
    nil))

;;;###autoload
(defun pylint-add-menu-items ()
  (let ((map (cond
              ((boundp 'py-mode-map) py-mode-map)
              ((boundp 'python-mode-map) python-mode-map))))
  
    (define-key map [menu-bar Python pylint-separator]
      '("--" . pylint-seperator))
    (define-key map [menu-bar Python next-error]
      '("Next error" . next-error))
    (define-key map [menu-bar Python prev-error]
      '("Previous error" . previous-error))
    (define-key map [menu-bar Python lint]
      '("Pylint" . pylint))
    nil))

(provide 'pylint)

;;; pylint.el ends here
