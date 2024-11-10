.. _pyreverse:

=========
Pyreverse
=========

``pyreverse`` analyzes your source code and generates package and class diagrams.

It supports output to ``.dot``/``.gv``, ``.puml``/``.plantuml`` (PlantUML) and ``.mmd``/``.html`` (MermaidJS) file formats.
If Graphviz (or the ``dot`` command) is installed, all `output formats supported by Graphviz <https://graphviz.org/docs/outputs/>`_
can be used as well. In this case, ``pyreverse`` first generates a temporary ``.gv`` file, which is then
fed to Graphviz to generate the final image.

.. toctree::
  :caption: Pyreverse
  :maxdepth: 3
  :titlesonly:
  :hidden:

  configuration
  output_examples
