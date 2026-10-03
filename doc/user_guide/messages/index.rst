.. _messages:

########
Messages
########

.. toctree::
  :maxdepth: 1
  :hidden:

  messages_overview.rst
  message_control.rst

Messages categories
===================

Pylint can emit various messages. These are categorized according
to categories corresponding to bit-encoded exit codes:

* :ref:`Fatal <fatal-category>` (1)
* :ref:`Error <error-category>` (2)
* :ref:`Warning <warning-category>` (4)
* :ref:`Convention <convention-category>` (8)
* :ref:`Refactor <refactor-category>` (16)
* :ref:`Information <information-category>` (NA)

An overview of these messages can be found in :ref:`messages-overview`

Disabling messages
==================

``pylint`` has an advanced message control for its checks, offering the ability
to enable / disable a message either from the command line or from the configuration
file, as well as from the code itself.

For more detail see :ref:`message-control`
