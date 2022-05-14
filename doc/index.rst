Pylint documentation
====================

Pylint is a `static code analyser`_ for python 2 or 3. Only python interpreter above 3.7.2 are supported
in the latest version.

Pylint analyses your code without actually running it. It checks for errors, enforces a coding
standard, looks for `code smells`_, and can make suggestions about how the code could be refactored.

Project that you might want to use alongside pylint include flake8_ (faster and simpler checks
with very few false positives), mypy_, pyright_ or pyre_ (typing checks), bandit_ (security
oriented checks), black_ and isort_ (auto-formatting).

.. _flake8: https://gitlab.com/pycqa/flake8/
.. _bandit: https://github.com/PyCQA/bandit
.. _mypy: https://github.com/python/mypy
.. _pyright: https://github.com/microsoft/pyright
.. _pyre: https://github.com/facebook/pyre-check
.. _black: https://github.com/psf/black
.. _isort: https://pycqa.github.io/isort/
.. _`static code analyser`: https://en.wikipedia.org/wiki/Static_code_analysis
.. _`code smells`: https://martinfowler.com/bliki/CodeSmell.html

Pylint can infer actual values from your code using it's internal code representation (astroid).
If your code is ``import logging as argparse``, Pylint will know that ``argparse.error(...)``
is in fact a logging call and not an argparse call.

Pylint isn't smarter than you: it may warn you about things that you have
conscientiously done or checks for some things that you don't care about.
During adoption, especially in a legacy project where pylint was never enforced,
it's best to start with the ``--errors-only`` flag, then disable
convention and refactor message with ``--disable=C,R`` and progressively
re-evaluate and re-enable messages as your priorities evolve.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   tutorial
   user_guide/index.rst
   how_tos/index.rst
   messages/index.rst
   technical_reference/index.rst
   development_guide/index.rst
   additional_commands/index.rst
   faq
   contact/index
   whatsnew/index.rst
