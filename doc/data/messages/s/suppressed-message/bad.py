### This is a contrived example, to show how suppressed-message works.
### First we enable all messages
# pylint: enable=all

### Here we disable two messages so we get two warnings
# pylint: disable=locally-disabled, useless-suppression # [suppressed-message, suppressed-message]

### Here we disable a message, so we get a warning for suppressed-message again.
"A"  # pylint: disable=pointless-statement # [suppressed-message, suppressed-message]
