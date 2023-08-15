*************************
 What's New in Pylint 3.0
*************************

.. toctree::
   :maxdepth: 2

:Release: 3.0.0
:Date: TBA


Summary -- Release highlights
=============================

Pylint now provides some important usability and performance improvements,
along with enacting necessary breaking changes and long-announced deprecations.

There's going to be frequent beta releases,
before the official releases, everyone is welcome to try the betas
so we find problems before the actual release.

The required ``astroid`` version is now 3.0.0. See the
`astroid changelog <https://pylint.readthedocs.io/projects/astroid/en/latest/changelog.html#what-s-new-in-astroid-3-0-0>`_
for additional fixes, features, and performance improvements applicable to pylint.

A new ``json2`` reporter has been added. It features an enriched output that is
easier to parse and provides more info, here's a sample output.

.. code-block:: json

    {
        "messages": [
            {
                "type": "convention",
                "symbol": "line-too-long",
                "message": "Line too long (1/2)",
                "messageId": "C0301",
                "confidence": "HIGH",
                "module": "0123",
                "obj": "",
                "line": 1,
                "column": 0,
                "endLine": 1,
                "endColumn": 4,
                "path": "0123",
                "absolutePath": "0123"
            }
        ],
        "statistics": {
            "messageTypeCount": {
                "fatal": 0,
                "error": 0,
                "warning": 0,
                "refactor": 0,
                "convention": 1,
                "info": 0
            },
            "modulesLinted": 1,
            "score": 5.0
        }
    }

.. towncrier release notes start
