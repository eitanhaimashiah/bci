BCI CLI Reference
=================

The ``bci`` package provides a command-line interface:

.. code:: bash

    $ python -m bci [OPTIONS] [COMMAND] [ARGS]
    ...

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

To see its version, run:

.. code:: bash

    $ python -m bci --version
    bci, version 0.1.0

The ``run_server`` Command
--------------------------

The ``run_server`` command receives an address in the form ip_address:port and a data
directory, and starts listening on that address for connections. When a
connection is accepted, the server receives its data containing a user's thought,
and writes it to the appropriate path on disk. Particularly, when user ``u`` thinks the
thought ``t`` at time ``d``, the server writes the thought to disk as
``data_dir/u/d.txt``. Note that the server keeps running until control+C is hit.

.. code:: bash

    $ python -m bci run_server "127.0.0.1:5000" data/

The ``upload_thought`` Command
------------------------------

The ``upload_thought`` command receives a server's address in the form ip_address:port,
a user ID, and a thought. It connects to the server, sends this data, and finally
prints ``done``; if an error occurs, it prints the error.

.. code:: bash

    $ python -m bci upload_thought "127.0.0.1:5000" 1 "I'm sleepy"
    done

The ``run_webserver`` Command
-----------------------------

The ``run_webserver`` command receives an address in the form ip_address:port and a
data directory, and starts a web server on that address, serving that data. When one
run the web server and browses its index (e.g. open a browser and go to
http://127.0.0.1:8000), a list of all the users available is presented. Similarly, when
one browses ``/users/<id>``, a table of that user's thoughts is presented. Note that the
web server keeps running until control+C is hit.

.. code:: bash

    $ python -m bci run_webserver "127.0.0.1:8000" data/
     * Serving Flask app "project.web" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 199-477-134
    127.0.0.1 - - [12/Dec/2019 20:15:37] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [12/Dec/2019 20:15:39] "GET /users/3 HTTP/1.1" 200 -
    ....
