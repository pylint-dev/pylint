A new ``json2`` reporter has been added. It features a more enriched output that is
easier to parse and provides more info.

Compared to ``json`` the only changes are that messages are now under the ``"messages"``
key and that ``"message-id"`` now follows the camelCase convention and is renamed to
``"messageId"``.
The new reporter also reports the "score" of the modules you linted as defined by the
``evaluation`` option and provides statistics about the modules you linted.

We encourage users to use the new reporter as the ``json`` reporter will no longer
be maintained.

Closes #4741
