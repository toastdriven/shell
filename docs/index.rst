.. shell documentation master file, created by
   sphinx-quickstart on Sun Jun  2 12:36:25 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

shell's Documentation
=====================

"""A better way to run shell commands in Python."""

Built because every time I go to use `subprocess`_, I spend more time in the
docs & futzing around than actually implementing what I'm trying to get done.

Dare I say: "shell commands for humans"? *gasp*

.. _`subprocess`: http://docs.python.org/2.7/library/subprocess.html


Philosophy
----------

* Makes running commands more natural
* Assumes you care about the output/errors by default
* Covers the 80% case of running commands
* A nicer API
* Works on Linux/OS X (untested on Windows but might work?)


Contents:

.. toctree::
   :maxdepth: 2

   tutorial
   shell_api
   testing
   contributing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

