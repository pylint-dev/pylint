.. _write_a_checker:

How to Write a Checker
======================
You can find some simple examples in the distribution
(`custom.py <https://github.com/pylint-dev/pylint/blob/main/examples/custom.py>`_
,
`custom_raw.py <https://github.com/pylint-dev/pylint/blob/main/examples/custom_raw.py>`_
and
`deprecation_checker.py <https://github.com/pylint-dev/pylint/blob/main/examples/deprecation_checker.py>`_).

.. TODO Create custom_token.py

There are three kinds of checkers:

* Raw checkers, which analyse each module as a raw file stream.
* Token checkers, which analyse a file using the list of tokens that
  represent the source code in the file.
* AST checkers, which work on an AST representation of the module.

The AST representation is provided by the ``astroid`` library.
``astroid`` adds additional information and methods
over ``ast`` in the standard library,
to make tree navigation and code introspection easier.

.. TODO Writing a Raw Checker

.. TODO Writing a Token Checker

Writing an AST Checker
----------------------
Let's implement a checker to make sure that all ``return`` nodes in a function
return a unique constant.
Firstly we will need to fill in some required boilerplate:

.. code-block:: python

  import astroid
  from astroid import nodes
  from typing import TYPE_CHECKING, Optional

  from pylint.checkers import BaseChecker

  if TYPE_CHECKING:
      from pylint.lint import PyLinter


  class UniqueReturnChecker(BaseChecker):

      name = "unique-returns"
      msgs = {
          "W0001": (
              "Returns a non-unique constant.",
              "non-unique-returns",
              "All constants returned in a function should be unique.",
          ),
      }
      options = (
          (
              "ignore-ints",
              {
                  "default": False,
                  "type": "yn",
                  "metavar": "<y or n>",
                  "help": "Allow returning non-unique integers",
              },
          ),
      )


So far we have defined the following required components of our checker:

* A name. The name is used to generate a special configuration
   section for the checker, when options have been provided.

* A message dictionary. Each checker is being used for finding problems
   in your code, the problems being displayed to the user through **messages**.
   The message dictionary should specify what messages the checker is
   going to emit. See `Defining a Message`_ for the details about defining a new message.

We have also defined an optional component of the checker.
The options list defines any user configurable options.
It has the following format::

    options = (
        ("option-symbol", {"argparse-like-kwarg": "value"}),
    )


* The ``option-symbol`` is a unique name for the option.
  This is used on the command line and in config files.
  The hyphen is replaced by an underscore when used in the checker,
  similarly to how you would use  ``argparse.Namespace``:

  .. code-block:: python

    if not self.linter.config.ignore_ints:
        ...

Next we'll track when we enter and leave a function.

.. code-block:: python

  def __init__(self, linter: Optional["PyLinter"] = None) -> None:
      super().__init__(linter)
      self._function_stack = []

  def visit_functiondef(self, node: nodes.FunctionDef) -> None:
      self._function_stack.append([])

  def leave_functiondef(self, node: nodes.FunctionDef) -> None:
      self._function_stack.pop()

In the constructor we initialise a stack to keep a list of return nodes
for each function.
An AST checker is a visitor, and should implement
``visit_<lowered class name>`` or ``leave_<lowered class name>``
methods for the nodes it's interested in.
In this case we have implemented ``visit_functiondef`` and ``leave_functiondef``
to add a new list of return nodes for this function,
and to remove the list of return nodes when we leave the function.

Finally we'll implement the check.
We will define a ``visit_return`` function,
which is called with an ``.astroid.nodes.Return`` node.

.. _astroid_extract_node:
.. TODO We can shorten/remove this bit once astroid has API docs.

We'll need to be able to figure out what attributes an
``.astroid.nodes.Return`` node has available.
We can use ``astroid.extract_node`` for this::

  >>> node = astroid.extract_node("return 5")
  >>> node
  <Return l.1 at 0x7efe62196390>
  >>> help(node)
  >>> node.value
  <Const.int l.1 at 0x7efe62196ef0>

We could also construct a more complete example::

  >>> node_a, node_b = astroid.extract_node("""
  ... def test():
  ...     if True:
  ...         return 5 #@
  ...     return 5 #@
  ... """)
  >>> node_a.value
  <Const.int l.4 at 0x7efe621a74e0>
  >>> node_a.value.value
  5
  >>> node_a.value.value == node_b.value.value
  True

For ``astroid.extract_node``, you can use ``#@`` at the end of a line to choose which statements will be extracted into nodes.

For more information on ``astroid.extract_node``,
see the `astroid documentation <https://pylint.readthedocs.io/projects/astroid/en/latest/>`_.

Now we know how to use the astroid node, we can implement our check.

.. code-block:: python

  def visit_return(self, node: nodes.Return) -> None:
      if not isinstance(node.value, nodes.Const):
          return
      for other_return in self._function_stack[-1]:
          if node.value.value == other_return.value.value and not (
              self.linter.config.ignore_ints and node.value.pytype() == int
          ):
              self.add_message("non-unique-returns", node=node)

      self._function_stack[-1].append(node)

Once we have established that the source code has failed our check,
we use ``~.BaseChecker.add_message`` to emit our failure message.

Finally, we need to register the checker with pylint.
Add the ``register`` function to the top level of the file.

.. code-block:: python

  def register(linter: "PyLinter") -> None:
      """This required method auto registers the checker during initialization.
      :param linter: The linter to register the checker to.
      """
      linter.register_checker(UniqueReturnChecker(linter))

We are now ready to debug and test our checker!

Providing an automatic fix
--------------------------
A message can come with a fix that ``pylint --fix`` applies (see :ref:`autofix`).
To give a message a fix, add a *fixer* to its checker: a method named ``fix_``
followed by the symbol of the message, with underscores instead of dashes. Like
``visit_`` methods, pylint finds it by its name. The fixer of
``compare-length-to-zero`` is ``fix_compare_length_to_zero``:

.. code-block:: python

  from pylint.message import Applicability, Edit, Fix, source_segment

  def visit_compare(self, node: nodes.Compare) -> None:
      # Looking for: len(basket) == 0
      ...
      self.add_message("compare-length-to-zero", node=node)

  def fix_compare_length_to_zero(self, node: nodes.Compare, **kwargs: Any) -> Fix | None:
      basket = source_segment(node.left.args[0])
      return Fix.create(
          "Use 'not' to check if the collection is empty",
          Edit.replace(node, f"not ({basket})"),
          applicability=Applicability.UNSAFE,
      )

The fixer receives the node of the message, and the other arguments given to
``add_message`` as keyword arguments: ``line``, ``args``, ``confidence``,
``col_offset``, ``end_lineno`` and ``end_col_offset``. A token checker, whose
messages have no node, can use ``line``. The fixer returns a ``Fix``, or
``None`` when this message cannot be fixed. It is only called when the message
is enabled, so a disabled message costs nothing.

A fix is a list of ``Edit``, each one replacing a part of the file with new text.
The edits of a fix are applied together or not at all. A message with a fixer is
shown as fixable in its documentation and in ``pylint --help-msg``. A ``fix_``
method that does not match a message of the checker is an error, so a typo in
its name does not go unnoticed.

Some messages can never be fixed automatically, because fixing them needs a
human decision. Say so with ``NeverFixable`` in place of the fixer, with the
reason shown to the users on the page of the message and in
``pylint --help-msg``:

.. code-block:: python

  from pylint.message import NeverFixable

  class FruitBasketChecker(BaseChecker):
      fix_too_many_fruits = NeverFixable(
          "Choosing which fruits to take out of the basket needs a human decision."
      )

A message without a fixer and without ``NeverFixable`` has no fix yet.

Some rules for writing a fix:

* ``Edit.replace``, ``Edit.delete``, ``Edit.insert_before`` and
  ``Edit.insert_after`` take a node and return ``None`` when the node has no
  position in the file, for example a node created by an astroid brain.
  ``Fix.create`` then returns ``None`` too, and the message has no fix. Only
  edit the file of the message: a fix touching a node inferred from another file
  is dropped.
* Build the new text from ``source_segment(node)``, the code exactly as the
  user wrote it, quotes and comments included. Don't use ``node.as_string()``
  for code that already exists: it rewrites the quotes and spacing, and drops
  comments.
* The parentheses around an expression are not part of its node: in
  ``len((apple + pear))``, the code of the argument is ``apple + pear``. Add
  parentheses when the new code needs them, like ``not (basket)`` above.
  Without them, ``apple + pear * 2`` would not mean ``(apple + pear) * 2``.
* Choose the ``applicability`` carefully. ``SAFE`` is only for fixes that can
  never change what the code does. A fix that relies on inference, or that may
  remove a comment, is ``UNSAFE``, and its documentation should say why.
  ``DISPLAY_ONLY`` is for suggestions that are never applied. The default is
  ``UNSAFE``. The applicability can be different for each message: a fix can
  be safe for a list and unsafe for an unknown type.
* Don't format the new code, the user runs a formatter afterwards.

* To change a bracket, a comma or another token that is not a node, use
  ``source_tokens(node)``: the tokens of the code of the node, comments included,
  with positions ready for an ``Edit``. ``Edit(*token.start, *token.end, "")``
  removes a token.

Columns of an ``Edit`` count UTF-8 bytes, like the ``col_offset`` of astroid
nodes. A token checker gets character columns from ``tokenize`` and should use
``Edit.from_character_columns``.

Testing a fix
~~~~~~~~~~~~~
A fix is tested in three places:

* **Functional tests.** When a functional test emits messages with fixes, the
  test runs ``pylint --fix`` on a copy of the file and compares the result with
  the ``.fixed`` file next to it. Running
  ``python tests/test_functional.py --update-functional-output -k <test>`` writes
  it for you. The test also fails if the fixes produce invalid code or never stop
  changing the file. An unsafe fix must be tested too: the ``.rc`` file of a test
  emitting one needs ``unsafe-fixes=yes`` in its ``[MAIN]`` section.
* **The documentation examples.** Running ``pylint --fix --unsafe-fixes`` on the
  ``bad.py`` example of the message must make the message go away.
* **The documentation.** A fixable message needs a ``fix.rst`` file next to its
  ``bad.py`` and ``good.py`` examples, telling what the fix does and why it is
  safe or unsafe. It is shown on the page of the message.

See the ``use-a-generator`` message for an example of all three.

Debugging a Checker
-------------------
It is very simple to get to a point where we can use ``pdb``.
We'll need a small test case.
Put the following into a Python file:

.. code-block:: python

  def test():
      if True:
          return 5
      return 5

  def test2():
      if True:
          return 1
      return 5

After inserting pdb into our checker and installing it,
we can run pylint with only our checker::

  $ pylint --load-plugins=my_plugin --disable=all --enable=non-unique-returns test.py
  (Pdb)

Now we can debug our checker!

.. Note::

    ``my_plugin`` refers to a module called ``my_plugin.py``.
    The preferred way of making this plugin available to pylint is
    by installing it as a package. This can be done either from a packaging index like
    ``PyPI`` or by installing it from a local source such as with ``pip install``.

    Alternatively, the plugin module can be made available to pylint by
    putting this module's parent directory in your ``PYTHONPATH``
    environment variable.

    If your pylint config has an ``init-hook`` that modifies
    ``sys.path`` to include the module's parent directory, this
    will also work, but only if either:

    * the ``init-hook`` and the ``load-plugins`` list are both
      defined in a configuration file, or...
    * the ``init-hook`` is passed as a command-line argument and
      the ``load-plugins`` list is in the configuration file

    So, you cannot load a custom plugin by modifying ``sys.path`` if you
    supply the ``init-hook`` in a configuration file, but pass the module name
    in via ``--load-plugins`` on the command line.
    This is because pylint loads plugins specified on command
    line before loading any configuration from other sources.

Defining a Message
------------------

Pylint message is defined using the following format::

   msgs = {
       "E0401": ( # message id
        "Unable to import %s", # template of displayed message
        "import-error", # message symbol
        "Used when pylint has been unable to import a module.",  # Message description
        { # Additional parameters:
             # message control support for the old names of the messages:
            "old_names": [("F0401", "old-import-error")]
            "minversion": (3, 5), # No check under this version
            "maxversion": (3, 7), # No check above this version
        },
    ),

The message is then formatted using the ``args`` parameter from ``add_message`` i.e. in
``self.add_message("import-error", args=module_we_cant_import, node=importnode)``, the value in ``module_we_cant_import`` say ``patglib`` will be interpolled and the final result will be:
``Unable to import patglib``


* The ``message-id`` should be a 4-digit number,
  prefixed with a **message category**.
  There are multiple message categories,
  these being ``C``, ``W``, ``E``, ``F``, ``R``,
  standing for ``Convention``, ``Warning``, ``Error``, ``Fatal`` and ``Refactoring``.
  The 4 digits should not conflict with existing checkers
  and the first 2 digits should consistent across the checker (except shared messages).
  It is safe to use 51-99 as the first 2 digits for custom checkers because this range is reserved for them.

* The ``displayed-message`` is used for displaying the message to the user,
  once it is emitted.

* The ``message-symbol`` is an alias of the message id
  and it can be used wherever the message id can be used.

* The ``message-help`` is used when calling ``pylint --help-msg``.

Optionally message can contain optional extra options:

* The ``old_names`` option permits to change the message id or symbol of a message without breaking the message control used on the old messages by users. The option is specified as a list
  of tuples (``message-id``, ``old-message-symbol``) e.g. ``{"old_names": [("F0401", "old-import-error")]}``.
  The symbol / msgid association must be unique so if you're changing the message id the symbol also need to change and you can generally use the ``old-`` prefix for that.

* The ``minversion`` or ``maxversion`` options specify minimum or maximum version of python
  relevant for this message. The option value is specified as tuple with major version number
  as first number and minor version number as second number e.g. ``{"minversion": (3, 5)}``

* The ``shared`` option enables sharing message between multiple checkers. As mentioned
  previously, normally the message cannot be shared between multiple checkers.
  To allow having message shared between multiple checkers, the ``shared`` option must
  be set to ``True``.

Parallelize a Checker
---------------------

``BaseChecker`` has two methods ``get_map_data`` and ``reduce_map_data`` that
permit to parallelize the checks when used with the ``-j`` option. If a checker
actually needs to reduce data it should define ``get_map_data`` as returning
something different than ``None`` and let its ``reduce_map_data`` handle a list
of the types returned by ``get_map_data``.

An example can be seen by looking at ``pylint/checkers/similar.py``.

Testing a Checker
-----------------
Pylint is very well suited to test driven development.
You can implement the template of the checker,
produce all of your test cases and check that they fail,
implement the checker,
then check that all of your test cases work.

Pylint provides a ``pylint.testutils.CheckerTestCase``
to make test cases very simple.
We can use the example code that we used for debugging as our test cases.

.. code-block:: python

  import astroid
  import my_plugin
  import pylint.testutils


  class TestUniqueReturnChecker(pylint.testutils.CheckerTestCase):
      CHECKER_CLASS = my_plugin.UniqueReturnChecker

      def test_finds_non_unique_ints(self):
          func_node, return_node_a, return_node_b = astroid.extract_node("""
          def test(): #@
              if True:
                  return 5 #@
              return 5 #@
          """)

          self.checker.visit_functiondef(func_node)
          self.checker.visit_return(return_node_a)
          with self.assertAddsMessages(
              pylint.testutils.MessageTest(
                  msg_id="non-unique-returns",
                  node=return_node_b,
              ),
          ):
              self.checker.visit_return(return_node_b)

      def test_ignores_unique_ints(self):
          func_node, return_node_a, return_node_b = astroid.extract_node("""
          def test(): #@
              if True:
                  return 1 #@
              return 5 #@
          """)

          with self.assertNoMessages():
              self.checker.visit_functiondef(func_node)
              self.checker.visit_return(return_node_a)
              self.checker.visit_return(return_node_b)


Once again we are using ``astroid.extract_node`` to
construct our test cases.
``pylint.testutils.CheckerTestCase`` has created the linter and checker for us,
we simply simulate a traversal of the AST tree
using the nodes that we are interested in.
