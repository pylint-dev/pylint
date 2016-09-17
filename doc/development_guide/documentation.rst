.. -*- coding: utf-8 -*-
==============
 Building the documentation
==============

When you would want to build the documentation for your self, you certainly can. Here's how...

The bare minimum
----------------

.. sourcecode:: bash

  $ python3 -m virtualenv venv
  $ . venv/bin/activate
  $ pip install Sphinx
  $ git clone https://github.com/PyCQA/pylint
  $ cd pylint
  $ python3 setup.py install
  $ cd doc
  $ make html

