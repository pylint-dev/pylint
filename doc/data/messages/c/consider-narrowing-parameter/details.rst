Passing a whole object when only one part of it is needed ties the function
to the object's structure for no benefit: this is sometimes called *stamp
coupling*. Callers must build (or know about) the whole object even when they
only have the one value the function really needs, which makes the function
harder to reuse and to test. Accepting the value itself (*data coupling*)
keeps the function independent.

The suggestion is only emitted when a single attribute is used. If the
function reads several attributes of the parameter, passing the whole object
is often the clearer design (see the *Preserve Whole Object* refactoring from
Martin Fowler's catalog).

The checker cannot know that an attribute is a structural back-reference
(like the ``parent`` of a tree node) whose narrowing would lose information,
so such parameters are still reported. Functions whose signature is imposed
by a convention or a framework can be excluded with the
``ignored-function-names`` option::

    [REFACTORING]
    ignored-function-names=(visit|leave)_.*
