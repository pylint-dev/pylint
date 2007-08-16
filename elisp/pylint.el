(require 'compile)

;; adapted from pychecker for pylint
(defun pylint-python-hook ()
  (defun pylint ()
    "Run pylint against the file behind the current buffer after
    checking if unsaved buffers should be saved."
    
    (interactive)
    (let* ((file (buffer-file-name (current-buffer)))
	   (command (concat "pylint --output-format=parseable \"" file "\"")))
      (save-some-buffers (not compilation-ask-about-save) nil) ; save  files.
      (compile-internal command "No more errors or warnings" "pylint")))
;;  (local-set-key [f1] 'pylint)
;;  (local-set-key [f2] 'previous-error)
;;  (local-set-key [f3] 'next-error)

  (define-key
    py-mode-map
    [menu-bar Python pylint-separator]
    '("--" . pylint-seperator))

  (define-key
    py-mode-map
    [menu-bar Python next-error]
    '("Next error" . next-error))
  (define-key
    py-mode-map
    [menu-bar Python prev-error]
    '("Previous error" . previous-error))
  (define-key
    py-mode-map
    [menu-bar Python lint]
    '("Pylint" . pylint))

  )

(add-hook 'python-mode-hook 'pylint-python-hook)
