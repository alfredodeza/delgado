
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

