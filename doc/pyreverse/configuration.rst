.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pyreverse_configuration.py'.



Pyreverse Configuration
^^^^^^^^^^^^^^^^^^^^^^^


--all-ancestors
"""""""""""""""
*Show all ancestors of all classes in <projects>.*

**Default:**  ``None``


--all-associated
""""""""""""""""
*Show all classes associated with the target classes, including indirect associations.*

**Default:**  ``None``


--class
"""""""
*Create a class diagram with all classes related to <class>; this uses by default the options -ASmy*

**Default:**  ``None``


--color-palette
"""""""""""""""
*Comma separated list of colors to use for the package depth coloring.*

**Default:**  ``('#77AADD', '#99DDFF', '#44BB99', '#BBCC33', '#AAAA00', '#EEDD88', '#EE8866', '#FFAABB', '#DDDDDD')``


--colorized
"""""""""""
*Use colored output. Classes/modules of the same package get the same color.*

**Default:**  ``False``


--filter-mode
"""""""""""""
*Filter attributes and functions according to <mode>. Correct modes are:
'PUB_ONLY' filter all non public attributes [DEFAULT], equivalent to PRIVATE+SPECIAL
'ALL' no filter
'SPECIAL' filter Python special functions except constructor
'OTHER' filter protected and private attributes*

**Default:**  ``PUB_ONLY``


--ignore
""""""""
*Files or directories to be skipped. They should be base names, not paths.*

**Default:**  ``('CVS',)``


--max-color-depth
"""""""""""""""""
*Use separate colors up to package depth of <depth>. Higher depths will reuse colors.*

**Default:**  ``2``


--module-names
""""""""""""""
*Include module name in the representation of classes.*

**Default:**  ``None``


--no-standalone
"""""""""""""""
*Only show nodes with connections.*

**Default:**  ``False``


--only-classnames
"""""""""""""""""
*Don't show attributes and methods in the class boxes; this disables -f values.*

**Default:**  ``False``


--output
""""""""
*Create a *.<format> output file if format is available. Available formats are: .dot, .puml, .plantuml, .mmd, .html. Any other format will be tried to be created by using the 'dot' command line tool, which requires a graphviz installation. In this case, these additional formats are available (see `Graphviz output formats <https://graphviz.org/docs/outputs/>`_).*

**Default:**  ``dot``


--output-directory
""""""""""""""""""
*Set the output directory path.*

**Default:** ``""``


--project
"""""""""
*Set the project name. This will later be appended to the output file names.*

**Default:** ``""``


--show-ancestors
""""""""""""""""
*Show <ancestor> generations of ancestor classes not in <projects>.*

**Default:**  ``None``


--show-associated
"""""""""""""""""
*Show <association_level> levels of associated classes not in <projects>.*

**Default:**  ``None``


--show-builtin
""""""""""""""
*Include builtin objects in representation of classes.*

**Default:**  ``False``


--show-stdlib
"""""""""""""
*Include standard library objects in representation of classes.*

**Default:**  ``False``


--source-roots
""""""""""""""
*Add paths to the list of the source roots. Supports globbing patterns. The source root is an absolute path or a path relative to the current working directory used to determine a package namespace for modules located under the source root.*

**Default:**  ``()``


--verbose
"""""""""
*Makes pyreverse more verbose/talkative. Mostly useful for debugging.*

**Default:**  ``False``
