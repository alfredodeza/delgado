
delgado
=======
Listen for commands over a unix socket and execute them in the terminal.

It solves the problem of text editors not wanting to bundle a real terminal
emulator.

``delgado`` requires valid JSON objects to be fired over a predetermined UDS
(Unix Domain Socket). Delgado has to know about what commands is authorized to
execute before running them, preventing arbitrary commands to be run).

A very simple listener allowed to run ``ls`` only would look like this::

    $ delgado run --allowed ls

On a different terminal, sending the JSON to that socket could be something
like::

    $ echo '{"ls": ["/tmp/foo"]}' | nc -U  /tmp/delgado.sock

The echo pipes over to ``nc`` (BSD Netcat) that in turn sends the information
to the socket. With the default logging levels, the output would then look like
this::

    $ delgado run --allowed ls
    --> Running command: [u'ls']

.. note::
    If you are planning on using ``netcat`` make sure it is the BSD version
    that has support for UDS (using the ``-U`` flag). The GNU version will not
    work. You can use *any* tool that can communicate over UDS.


Increasing Verbosity
--------------------
The command line tool uses a flag to control how much output it shows. By
default the level is ``INFO`` (just like normal logging in applications) and
can be raised all the way up to ``DEBUG``

This is how a debug level call would look like for running the ``pytest``
plugin::

    $ delgado --log debug pytest
    --> [debug] loading pytest
    --> [debug] creating a new connection



Plugins
-------

``pytest``
----------
``delgado`` was originally conceived to give support to ``pytest.vim`` so it
includes the ``pytest`` plugin that when called, it will listen for ``py.test``
commands only and execute them.

To listen for ``py.test`` commands, you would call the command like this::

    $ delgado pytest


Adding plugins
--------------
``delgado`` was built with some modularity in mind, by default you get the
``py.test`` plugin which will run the server and listen for ``py.test`` commands
only.

The plugins use ``setuptools`` entry points. If you want a new plugin to be
available, this is what it should have on its ``setup.py`` file::

    setup(
        ...
        entry_points = dict(
            delgado_handlers = [
                'my_command = my_package.my_module:MyClass',
            ],
        ),

The ``MyClass`` should be a class that accepts ``sys.argv`` as its argument,
``delgado`` will pass that in at instantiation and call a ``parse_args``
method.

This is how the ``py.test`` plugin looks like for example::


    class Pytest(object):

        help_menu = 'A handler for running py.test commands'
        _help = """
    Run a base socket listener that allows py.test commands.

    --socket-location   The location for the socket (defaults
                        to /tmp/pytest.sock)
        """

        def __init__(self, argv):
            self.argv = argv

        def parse_args(self):
            ...
