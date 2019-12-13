BCI API Reference
====================

This is BCI's API reference.

Server
------

.. method:: bci.run_server(address, data_dir)

    Receives an address (a tuple of the server's IP address and port) and a data
    directory, and starts listening on that address for connections. When a
    connection is accepted, the server receives its data containing a user's thought,
    and writes it to the appropriate path on disk. Particularly, when user ``u``
    thinks the thought ``t`` at time ``d``, the server writes the thought to disk as
    ``data_dir/u/d.txt``. Note that the server keeps running until control+C is hit.

Client
------

.. method:: bci.upload_thought(address, user, thought)

    Receives an address (a tuple of the server's IP address and port), a user ID,
    and a thought. It connects to the server, sends this data, and finally prints
    ``done``; if an error occurs, it prints the error.

Web
---

.. method:: bci.run_webserver(address, data_dir)

    Receives an address (a tuple of the server's IP address and port) and a data
    directory, and starts a web server on that address, serving that data. When one
    run the web server and browses its index (e.g. open a browser and go to
    http://127.0.0.1:8000), a list of all the users available is presented.
    Similarly, when one browses ``/users/<id>``, a table of that user's thoughts is
    presented. Note that the web server keeps running until control+C is hit.


Thought
-------

.. class:: bci.Thought

    Encapsulates ``Thought`` objects.

    .. method:: __repr__()

        Returns a string representation of this thought.

    .. method:: __str__()

        Returns a readable string representation of this thought.

    .. method:: __eq__(other)

        Returns true only if ``other``  is a ``Thought`` instance with similar
        attributes.

    .. method:: serialize()

        Returns bytes representing this thought, ready to be sent over the wire.

    .. method:: deserialize(data)

        Returns a new thought instance obtained by decoding the given bytes ``data``.

Connection
----------

.. class:: bci.utils.Connection

    Encapsulates ``Connection`` objects.

    .. method:: __repr__()

        Returns a string representation of this connection.

    .. method:: __enter__()

        Returns this connection.

    .. method:: __exit__()

        Calls ``close()`` method.

    .. method:: connect(host, port)

        Connects to the specified ``host`` and ``port``, and returns a ``Connection``
        object for this connection.

    .. method:: send(data)

        Sends ``data`` over the socket.

    .. method:: receive(size)

        Receives as many bytes as were specified by ``size``, or throws an
        exception if the connection was closed before all the data was received.

Listener
--------

.. class:: bci.utils.Listener

    Encapsulates ``Listener`` objects.

    .. method:: __repr__()

        Returns a string representation of this listener.

    .. method:: __enter__()

        Returns this listener after calling ``start()`` method.

    .. method:: __exit__()

        Calls ``stop()`` method.

    .. method:: start()

        Starts listening on the listener's ``host`` and ``port``.

    .. method:: stop()

        Stops listening and closes the socket.

    .. method:: accept()

        Waits for a connection, accepts it, and returns a ``Connection`` object.
