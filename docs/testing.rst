=============
Testing shell
=============

``shell`` maintains 100% passing tests at all times. That said, there are
undoubtedly bugs or odd configurations it doesn't cover.


Setup
=====

Getting setup to run tests (Python 2) looks like::

    $ git clone https://github.com/toastdriven/shell
    $ cd shell
    $ virtualenv env
    $ . env/bin/activate
    $ pip install mock==1.0.1
    $ pip install nose==1.3.0

Once that's setup, setting up for Python 3 looks like::

    $ virtualenv -p python3 env3
    $ . env3/bin/activate
    $ pip install mock==1.0.1
    $ pip install nose==1.3.0


Running the tests
=================

To run the tests, run the following::

    $ nosetests -s tests.py
