==============
shell Tutorial
==============

If you've ever tried to run a shell command in Python, you're likely unhappy
about it. The ``subprocess`` module, while a huge & consistent step forward
over the previous ways Python shelled out, has a rather painful interface.
If you're like me, you spent more time in the docs than you did writing working
code.

``shell`` tries to fix this, by glossing over the warts in the ``subprocess``
API & making running commands *easy*.


Installation
============

If you're developing in Python, you ought to be using `pip`_. Installing (from
your terminal) looks like::

    $ pip install shell

.. _`pip`: http://www.pip-installer.org/en/latest/


Quickstart
==========

For the impatient::

    >>> from shell import shell
    >>> ls = shell('ls')
    >>> for file in ls.output():
    ...     print file
    'another.txt'

    # Or if you need more control, the same code can be stated as...
    >>> from shell import Shell
    >>> sh = Shell()
    >>> sh.run('ls')
    >>> for file in sh.output():
    ...     print file
    'another.txt'


Getting Started
===============

Importing
---------

The first thing you'll need to do is import ``shell``. You can either use
the easy functional version::

    >>> from shell import shell

Or the class-based & extensible version::

    >>> from shell import Shell


Your First Command
------------------

Running a basic command is simple. Simply hand the command you'd use at the
terminal off to ``shell``::

    >>> from shell import shell
    >>> shell('touch hello_world.txt')

    # The class-based variant.
    >>> from shell import Shell
    >>> sh = Shell()
    >>> sh.run('touch hello_world.txt')

You should now have a ``hello_world.txt`` file created in your current
directory.


Reading Output
--------------

By default, ``shell`` captures output/errors from the command being run. You can
read the output & errors like so::

    >>> from shell import shell
    >>> sh = shell('ls /tmp')
    # Your output from these calls will vary...
    >>> sh.output()
    [
        'hello.txt',
        'world.py',
    ]
    >>> sh.errors()
    []

    # The class-based variant.
    >>> from shell import Shell
    >>> sh = Shell()
    >>> sh.run('ls /tmp')
    >>> sh.output()
    [
        'hello.txt',
        'world.py',
    ]
    >>> sh.errors()
    []

You can also look at what the process ID was & the return code.::

    >>> sh.pid
    15172
    >>> sh.code
    0

Getting a ``0`` from ``sh.code`` means a process finished sucessfully. Higher
integer return values generally mean there was an error.


Interactive
-----------

If the command is interactive, you can send it input as well.::

    >>> from shell import shell
    >>> sh = shell('cat -u', has_input=True)
    >>> sh.write('Hello, world!')
    >>> sh.output()
    [
        'Hello, world!'
    ]

    # The class-based variant.
    >>> from shell import Shell
    >>> sh = Shell(has_input=True)
    >>> sh.run('cat -u')
    >>> sh.write('Hello, world!')
    >>> sh.output()
    [
        'Hello, world!'
    ]

.. warning::

    You get one shot at sending input, after which the command will finish.
    Using ``shell`` for advanced, multi-prompt shell commands is likely is not
    a good option.


Failing Fast
------------

You can have non-zero exit codes propigate as exceptions::

    >>> from shell import shell
    >>> shell('ls /not/a/real/place', die=True)
	Traceback (most recent call last):
        ...
	shell.CommandError: Command exited with code 1
    >>> import sys
    >>> from shell import CommandError
    >>> try:
    >>>     shell('ls /also/definitely/fake', die=True)
    >>> except CommandError, e:
    >>>     print e.stderr
    >>>     sys.exit(e.code)
    ls: /also/definitely/fake: No such file or directory
    $ echo $?
    1


Chaining
--------

You can also chain calls together, if that suits you.::

    >>> from shell import shell
    >>> shell('cat -u', has_input=True).write('Hello, world!').output()
    [
        'Hello, world!'
    ]

    # The class-based variant.
    >>> from shell import Shell
    >>> Shell(has_input=True).run('cat -u').write('Hello, world!').output()
    [
        'Hello, world!'
    ]


Ignoring Large Output
---------------------

By default, ``shell`` captures all output/errors. If you have a command that
generates a large volume of output that you don't care about, you can ignore
it like so.::

    >>> from shell import shell
    >>> sh = shell('run_intensive_command -v', record_output=False, record_errors=False)
    >>> sh.code
    0

    # The class-based variant.
    >>> from shell import Shell
    >>> sh = Shell(record_output=False, record_errors=False)
    >>> sh.run('run_intensive_command -v')
    >>> sh.code
    0


What Now?
=========

If you need more advanced functionality, subclassing the ``Shell`` class is the
best place to start.

You can find more details about it in the :doc:`shell_api`.
