A ``no-member`` error means one of:

- pylint found a bug in your code
- the dependencies are not installed in pylint's environment
- the attribute lives in a C extension module, and pylint is refraining from
  importing it
- the attribute is generated dynamically

The only way to get an AST out of a C extension is to load it into the active
Python interpreter, which may run arbitrary code, so pylint does not do it by
default. If you accept that, tell it to load the module and build the AST from
it, one package at a time with :ref:`extension-pkg-allow-list <main-options>`
or for every extension with :ref:`unsafe-load-any-extension <main-options>`::

   $ pylint --extension-pkg-allow-list=your_c_extension
   $ pylint --unsafe-load-any-extension=y

Attributes missing from a C extension are reported as
:ref:`c-extension-no-member`, so you can also disable that message alone.

For attributes created at runtime, list them with
:ref:`generated-members <typecheck-options>`::

   $ pylint --generated-members=cv2.LINE_AA,sphinx.generated_member
