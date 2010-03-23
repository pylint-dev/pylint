;; Fixed bug where py-mode-map is undefined in Gnu Emacs 22 and 23
;; Yuen Ho Wong (2009)
;;
;; Modifications done by Yarosav O. Halchenko (2008):
;;  - enable user-visible variables
;; distributed under the same copyright/license terms as
;; pylint itself
;;
(require 'compile)

;; user definable variables
;; vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

(defgroup pylint nil
  "Emacs support for the Pylint Python checker"
  :group 'languages
  :prefix "pylint-")

(defcustom pylint-options "--output-format=parseable"
  "*Command line options to be used with pylint call"
  :type 'string
  :group 'pylint)


;; adapted from pychecker for pylint
(defun pylint-python-hook ()
  (defun pylint ()
    "Run pylint against the file behind the current buffer after
    checking if unsaved buffers should be saved."

    (interactive)
    (let* ((file (buffer-file-name (current-buffer)))
           (command (concat "pylint " pylint-options " \"" file "\"")))
      (save-some-buffers (not compilation-ask-about-save) nil) ; save  files.
      (compilation-start command)))

  (let ((python-mode-map (cond ((boundp 'py-mode-map) py-mode-map)
                               ((boundp 'python-mode-map) python-mode-map))))

    ;; shortcuts in the tradition of python-mode and ropemacs
    (define-key python-mode-map (kbd "C-c m l") 'pylint)
    (define-key python-mode-map (kbd "C-c m p") 'previous-error)
    (define-key python-mode-map (kbd "C-c m n") 'next-error)

  (let ((map))
    (if(boundp 'py-mode-map)
        (setq map py-mode-map)
      (setq map python-mode-map)
      (define-key
        map
        [menu-bar Python pylint-separator]
        '("--" . pylint-seperator))
      (define-key
        map
        [menu-bar Python next-error]
        '("Next error" . next-error))
      (define-key
        map
        [menu-bar Python prev-error]
        '("Previous error" . previous-error))
      (define-key
        map
        [menu-bar Python lint]
        '("Pylint" . pylint))
      ))
    ))

(add-hook 'python-mode-hook 'pylint-python-hook)
