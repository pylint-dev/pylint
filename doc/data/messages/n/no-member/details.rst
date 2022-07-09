If you are getting the dreaded ``no-member`` error, there is a possibility that
either:

- Pylint found a bug in your code
- You're launching Pylint without the dependencies installed in its environment.
- Pylint would need to lint a C extension module and is refraining to do so.

Linting C extension modules is not supported out of the box, especially since
pylint has no way to get an AST object out of the extension module.

But Pylint actually has a mechanism which you might use in case you
want to analyze C extensions. Pylint has a flag, called ``extension-pkg-allow-list``
(formerly ``extension-pkg-whitelist``), through which you can tell it to
import that module and to build an AST from that imported module::

   $ pylint --extension-pkg-allow-list=your_c_extension

Be aware though that using this flag means that extensions are loaded into the
active Python interpreter and may run arbitrary code, which you may not want. This
is the reason why we disable by default loading C extensions. In case you do not want
the hassle of passing C extensions module with this flag all the time, you
can enable ``unsafe-load-any-extension`` in your configuration file, which will
build AST objects from all the C extensions that Pylint encounters::

   $ pylint --unsafe-load-any-extension=y

Alternatively, since Pylint emits a separate error for attributes that cannot be
found in C extensions, ``c-extension-no-member``, you can disable this error for
your project.
