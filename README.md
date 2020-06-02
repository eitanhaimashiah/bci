![build status](https://travis-ci.org/eitanhaimashiah/bci.svg?branch=master)
![coverage](https://codecov.io/gh/eitanhaimashiah/bci/branch/master/graph/badge.svg)

# BCI

Brain Computer Interface (BCI) is a system that can read minds, and 
upload snapshots of cognitions. Our system includes 
a [client](#the-client), which streams cognition snapshots to 
a [server](#the-server), which then publishes them to 
a [message queue](#the-message-queue-and-the-parses), where multiple 
[parsers](#the-message-queue-and-the-parses) read the snapshot, parse 
various parts of it, and publish the parsed results, which are then 
saved to a [database](#the-database-and-the-savers). The results are 
then exposed via a RESTful [API](#the-api), which is consumed by 
a [CLI](#the-cli); there's alsoa [GUI](#the-gui), which visualizes the
results in various ways.

See [full documentation](https://bci.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:eitanhaimashiah/bci.git
    ...
    $ cd bci/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [bci] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```   

## Running the whole pipeline

1. To start the container of each component in the pipeline one by one, 
    just run: 

    ```sh
    $ ./scripts/run-pipeline.sh
    Starting pipeline...
    ...
    GUI is available at http://localhost:8080
    Run a client to upload a sample
    ```

2. Once the above is done, run a client to upload a sample:
    
    ```sh
    $ python -m bci.client upload-sample 'test_sample.mind'
    Sent the snapshot from December 4, 2019 at 10:08:07.339
    Sent the snapshot from December 4, 2019 at 10:08:07.412
    Sent the snapshot from December 4, 2019 at 10:08:07.476
    Sent the snapshot from December 4, 2019 at 10:08:07.541
    ...
    ```
   
3. Check out the GUI at `http://localhost:8080` to see the 
    uploaded sample.

4. To stop the whole pipeline, run:
    
    ```sh
    $ ./scripts/stop-pipeline.sh
    ...
    ```
    
## Usage

The `bci` package provides an application programming interface (API) 
alongside a command-line interface (CLI). The usage in each `bci`'s 
component is listed in the following sections.

All CLI commands accept the `-q` or `--quiet` flag to suppress output, 
and the `-t` or `--traceback` flag to show the full traceback when 
an exception is raised (by default, only the error message is printed, 
and the program exits with a non-zero code).

### The client
The client reads cognition snapshots from a sample file and streams 
them to the server. It is available as `bci.client` and exposes the 
following API:
    
```pycon
>>> from bci.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
… # upload path to host:port
```

And the following CLI:

```sh
$ python -m bci.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
…
```

### The server
The server accepts client connections, receives the uploaded samples 
and publishes them to its message queue. It is available as 
`bci.server` and exposes the following API:

```pycon
>>> from bci.server import run_server
>>> def print_message(message):
...     print(message)
>>> run_server(host='127.0.0.1', port=8000, publish=print_message)
… # listen on host:port and pass received messages to publish
```

And the following CLI:

```sh
$ python -m bci.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
…
```

### The Parsers
A collection of parsers which consume raw data from the message queue, 
parse various parts of it, and publish the parsed results to the 
message queue back. They are located in `bci.parsers`, and expose the 
following API:

```pycon
>>> from bci.parsers import run_parser
>>> data = … 
>>> result = run_parser('pose', data)
```

Which accepts a parser name and some raw data, as consumed from the 
message queue, and returns the result, as published to the message 
queue. It also provides the following CLI:

```sh
$ python -m bci.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
```

Which accepts a parser name and a path to some raw data, as consumed 
from the message queue, and prints the result, as published to the 
message queue (optionally redirecting it to a file). This way of 
invocation runs the parser exactly once; the CLI also supports running 
the parser as a service, which works with a message queue indefinitely.

The current available parsers are:

- *Pose* <br />
  Collects the translation and the rotation of the user's head at a 
  given timestamp.
- *Color Image* <br />
  Collects the color image of what the user was seeing at a given 
  timestamp.
- *Depth Image* <br />
  Collects the depth image of what the user was seeing at a given 
  timestamp.
- *Feelings* <br />
  Collects the feelings the user was experiencing at any timestamp.

#### Adding a new parser
To add a new parser, write a function starting with `parse_` or a 
class ending with `Parser` in a new module under the `bci.parsers` 
subpackage. The function / class should have an attribute named





### The message queue and the parses
<!-- TODO Provide documentation about how to add a new parser: 
what would I need to do to be able to have the parse command invoke 
my own code, and the run-parser command to run it as a service 
working with a message queue. -->

### The database and the savers

### The API
 
### The CLI

### The GUI
