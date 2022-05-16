.. _messages:

########
Messages
########

.. toctree::
  :maxdepth: 2
  :hidden:


  messages_list.rst
  message-control.rst

Pylint can emit various messages. These are categorized according
to categories corresponding to bit-encoded exit codes:

* :ref:`Fatal` (1)
* :ref:`Error` (2)
* :ref:`Warning` (4)
* :ref:`Convention` (8)
* :ref:`Refactor` (16)
* :ref:`Information` (NA)

A list of these messages can be found in :ref:`messages-list`

Disabling messages
==================

``pylint`` has an advanced message control for its checks, offering the ability
to enable / disable a message either from the command line or from the configuration
file, as well as from the code itself.

For more detail see :ref:`message-control`
