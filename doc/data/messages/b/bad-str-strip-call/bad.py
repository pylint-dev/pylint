"Hello World".strip("Hello")  # [bad-str-strip-call]
# >>> ' World'
"abcbc def bacabc".strip("abcbc ")  # [bad-str-strip-call]
# >>> 'def'
