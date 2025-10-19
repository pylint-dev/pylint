.. _message-control:

Messages control
================

In order to control messages, ``pylint`` accepts the following values:

* a symbolic message: ``no-member``, ``undefined-variable`` etc.

* a numerical ID: ``E1101``, ``E1102`` etc.

* The name of the group of checks. You can grab those with ``pylint --list-groups``.
  For example, you can disable / enable all the checks related to type checking, with
  ``typecheck`` or all the checks related to variables with ``variables``

* Corresponding category of the checks

  * ``C`` convention related checks
  * ``R`` refactoring related checks
  * ``W`` various warnings
  * ``E`` errors, for probable bugs in the code
  * ``F`` fatal, if an error occurred which prevented ``pylint`` from doing further processing.

* All the checks with ``all``

.. _block_disables:

Block disables
--------------

This describes how the pragma controls operate at a code level.

The pragma controls can disable / enable:

* All the violations on a single line

.. sourcecode:: python

    a, b = ... # pylint: disable=unbalanced-tuple-unpacking

* All the violations on the following line

.. sourcecode:: python

    # pylint: disable-next=unbalanced-tuple-unpacking
    a, b = ...

* All the violations in a single scope

.. sourcecode:: python

    def test():
        # Disable all the no-member violations in this function
        # pylint: disable=no-member
        ...

* All the violations in a `block`. For instance, each separate branch of an
  ``if`` statement is considered a separate block, as in the following example:

.. sourcecode:: python

    def meth5(self):
        # pylint: disable=no-member
        # no error
        print(self.bla)
        if self.blop:
            # pylint: enable=no-member
            # enable all no-members for this block
            print(self.blip)
        else:
            # This is affected by the scope disable
            print(self.blip)
        # pylint: enable=no-member
        print(self.blip)
        if self.blop:
            # pylint: disable=no-member
            # disable all no-members for this block
            print(self.blip)
        else:
            # This emits a violation
            print(self.blip)


* If the violation occurs on a block starting line, then it applies only to that line

.. sourcecode:: python

    if self.blop: # pylint: disable=no-member; applies only to this line
        # Here we get an error
        print(self.blip)
    else:
        # error
        print(self.blip)



Here's an example with all these rules in a single place:

.. sourcecode:: python

    """pylint option block-disable"""

    __revision__ = None

    class Foo(object):
        """block-disable test"""

        def __init__(self):
            pass

        def meth1(self, arg):
            """this issues a message"""
            print(self)

        def meth2(self, arg):
            """and this one not"""
            # pylint: disable=unused-argument
            print(self\
                  + "foo")

        def meth3(self):
            """test one line disabling"""
            # no error
            print(self.bla) # pylint: disable=no-member
            # error
            print(self.blop)

        def meth4(self):
            """test re-enabling"""
            # pylint: disable=no-member
            # no error
            print(self.bla)
            print(self.blop)
            # pylint: enable=no-member
            # error
            print(self.blip)

        def meth5(self):
            """test IF sub-block re-enabling"""
            # pylint: disable=no-member
            # no error
            print(self.bla)
            if self.blop:
                # pylint: enable=no-member
                # error
                print(self.blip)
            else:
                # no error
                print(self.blip)
            # no error
            print(self.blip)

        def meth6(self):
            """test TRY/EXCEPT sub-block re-enabling"""
            # pylint: disable=no-member
            # no error
            print(self.bla)
            try:
                # pylint: enable=no-member
                # error
                print(self.blip)
            except UndefinedName: # pylint: disable=undefined-variable
                # no error
                print(self.blip)
            # no error
            print(self.blip)

        def meth7(self):
            """test one line block opening disabling"""
            if self.blop: # pylint: disable=no-member
                # error
                print(self.blip)
            else:
                # error
                print(self.blip)
            # error
            print(self.blip)

        def meth8(self):
            """test late disabling"""
            # error
            print(self.blip)
            # pylint: disable=no-member
            # no error
            print(self.bla)
            print(self.blop)

        def meth9(self):
            """test next line disabling"""
            # no error
            # pylint: disable-next=no-member
            print(self.bla)
            # error
            print(self.blop)


.. _conflict-c0209-w1203:

C0209 and W1203 conflict
------------------------

These two messages are mutually exclusive when working with logging:

- **C0209** (`consider-using-f-string`) recommends using f-strings
- **W1203** (`logging-fstring-interpolation`) recommends using `%` formatting for performance reasons

This causes a conflict if both are enabled. You can resolve it by choosing one of the following:

- **Option 1:** Disable W1203 to allow f-strings in logging:

  .. code-block:: ini

      [MESSAGES CONTROL]
      disable=W1203

- **Option 2:** Disable C0209 to prefer `%` formatting in logging:

  .. code-block:: ini

      [MESSAGES CONTROL]
      disable=C0209

      
Detecting useless disables
--------------------------

As pylint gets better and false positives are removed,
disables that became useless can accumulate and clutter the code.
In order to clean them you can enable the ``useless-suppression`` warning.
