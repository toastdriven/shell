=====
shell
=====

"""A better way to run shell commands in Python."""

Built because every time I go to use `subprocess`_, I spend more time in the
docs & futzing around than actually implementing what I'm trying to get done.

.. _`subprocess`: http://docs.python.org/2.7/library/subprocess.html

Full docs are at https://shell.readthedocs.org/en/latest/.


Requirements
============

* Python 2.6+ or Python 3.3+


Usage
=====

If you just need to quickly run a command, you can use the ``shell`` shortcut
function::

    >>> from shell import shell
    >>> ls = shell('ls')
    >>> for file in ls.output():
    ...     print file
    'another.txt'

If you need to extend the behavior, you can also use the ``Shell`` object::

    >>> from shell import Shell
    >>> sh = Shell(has_input=True)
    >>> cat = sh.run('cat -u')
    >>> cat.write('Hello, world!')
    >>> cat.output()
    ['Hello, world!']

You can even chain calls if you'd like::

    >>> from shell import shell
    >>> shell('cat -u', has_input=True).write('Hello, world!').output()
    ['Hello, world!']


Installation
============

Using ``pip``, simply run::

    pip install shell


License
=======

New BSD
