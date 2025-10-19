.. _pyreverse:

=========
Pyreverse
=========

``pyreverse`` is a powerful tool that creates UML diagrams from your Python code. It helps you visualize:

- Package dependencies and structure
- Class hierarchies and relationships
- Method and attribute organization

For a detailed external guide explaining the meaning of each arrow and relationship, please see this `UML Class Diagram Arrows Guide <https://paulrumyancev.medium.com/uml-class-diagram-arrows-guide-37e4b1bb11e>`_.

Output Formats
==============

``pyreverse`` supports multiple output formats:

* Native formats:
    * ``.dot``/``.gv`` (Graphviz)
    * ``.puml``/``.plantuml`` (PlantUML)
    * ``.mmd``/``.html`` (MermaidJS)

* Additional formats (requires Graphviz installation):
    * All `Graphviz output formats <https://graphviz.org/docs/outputs/>`_ (PNG, SVG, PDF, etc.)
    * ``pyreverse`` first generates a temporary ``.gv`` file, which is then fed to Graphviz to generate the final image

Getting Started
===============

Check out the :doc:`configuration` guide to learn about available options, or see :doc:`output_examples`
for sample diagrams and common use cases.

.. toctree::
   :maxdepth: 2
   :caption: Pyreverse
   :titlesonly:
   :hidden:

   configuration
   output_examples
