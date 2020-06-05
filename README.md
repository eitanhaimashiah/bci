[![build status](https://travis-ci.org/eitanhaimashiah/bci.svg?branch=master)](https://travis-ci.org/eitanhaimashiah/bci)
[![coverage](https://codecov.io/gh/eitanhaimashiah/bci/branch/master/graph/badge.svg)](https://codecov.io/gh/eitanhaimashiah/bci)

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
>>> from bci.parsers import parse
>>> data = … 
>>> result = parse('pose', data)
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

```sh
$ python -m bci.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
```

The current available parsers are:

- **Pose** <br />
  Collects the translation and the rotation of the user's head at a 
  given timestamp.
  
- **Color Image** <br />
  Collects the color image of what the user was seeing at a given 
  timestamp.
  
- **Depth Image** <br />
  Collects the depth image of what the user was seeing at a given 
  timestamp.
  
- **Feelings** <br />
  Collects the feelings the user was experiencing at any timestamp.

#### Adding a new parser
To add a new parser, write a function starting with `parse_` or a 
class ending with `Parser` in a new module under the `parsers/` 
subpackage. The function / class should have an attribute named 
`field`, specifying the part of the snapshot this parser is 
interested in.

Here's `parsers/translation.py`:

```python
def parse_pose(context, snapshot):
    return snapshot['pose']

parse_pose.field = 'pose'
```

Here's `parsers/color_image.py` (our actual implementation defines
a function rather than a class):

```python
import pathlib
from PIL import Image

class ColorImageParser:
    field = 'color_image'

    def parse(self, context, snapshot):
        color_image = snapshot['color_image']
        size = color_image['width'], color_image['height']
        data = pathlib.Path(color_image['data']).read_bytes()
        result_path = context.path('color_image.jpg', is_raw=False)
        image = Image.frombytes('RGB', size, data)
        image.save(result_path)
        return {
            'path': str(result_path)
        }
```

After adding a parser with a certain field, one can simply use 
the above Parsers' CLI (commands `parse` and `run-parser`) on 
that field.

### The saver
The saver connects to a database, and saves the parsed results 
to it. It is available as `bci.saver` and exposes the following API:

```pycon
>>> from bci.saver import Saver
>>> saver = Saver(database_url)
>>> data = …
>>> saver.save('pose', data)
```

Which connects to a database, accepts a topic name and some data, 
as consumed from the message queue, and saves it to the database. 
It should also provide the following CLI:

```sh
$ python -m bci.saver save                     \
      -d/--database 'postgresql://bci:pass@127.0.01:5432' \
     'pose'                                       \
     'pose.result' 
```

Which accepts a topic name and a path to some raw data, as consumed 
from the message queue, and saves it to a database. This way of 
invocation runs the saver exactly once; the CLI should also support 
running the saver as a service, which works with a message queue 
indefinitely; it is then the saver's responsibility to subscribe to 
all the relevant topics it is capable of consuming and saving to the 
database.

```sh
$ python -m bci.saver run-saver  \
      'postgresql://bci:pass@127.0.01:5432' \
      'rabbitmq://127.0.0.1:5672/'
```

Note that the database URL is of the form `DB://USERNAME:PASSWORD@HOST:PORT`.

### The API
A RESTful API exposing the data available in the database. It is 
available as `bci.api` and exposes the following API:

```pycon
>>> from bci.api import run_api_server
>>> run_api_server(
...     host = '127.0.0.1',
...     port = 5000,
...     database_url = 'postgresql://bci:pass@127.0.01:5432',
... )
… # listen on host:port and serve data from database_url
```

And the following CLI:

```sh
$ python -m bci.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'postgresql://bci:pass@127.0.01:5432'
```

It supports the following endpoints:

- `GET /users`<br />
  Returns the list of all the supported users, including their IDs and 
  names only.

- `GET /users/user-id`<br />
  Returns the specified user's details: ID, name, birthday and gender.

- `GET /users/user-id/snapshots`<br />
  Returns the list of the specified user's snapshot IDs and datetimes 
  only.

- `GET /users/user-id/snapshots/snapshot-id`<br />
  Returns the specified snapshot's details: ID, datetime, and the available 
  results' names only (e.g. `pose`).

- `GET /users/user-id/snapshots/snapshot-id/result-name`<br />
  Returns the specified snapshot's result. It currently supports 
  `pose`, `color-image`, `depth-image` and `feelings`.
  
- `GET /users/user-id/snapshots/snapshot-id/result-name/data`<br />
  Returns the binary data for snapshot's results that have such data.
  It supports `color-image` and `depth-image`.

### The CLI
The CLI consumes the API, and reflects it using command-line.

```sh
$ python -m cortex.cli get-users
…
$ python -m cortex.cli get-user 1
…
$ python -m cortex.cli get-snapshots 1
…
$ python -m cortex.cli get-snapshot 1 2
…
$ python -m cortex.cli get-result 1 2 'pose'
…
```

All commands accept the `-h/--host` and `-p/--port` flags to 
configure the host and port, but default to the API's address.
The `get-result` command also accepts the `-s/--save` flag that, 
if specified, receives a path, and saves the result's data to that 
path.

### The GUI
The GUI consume the API and reflects it using a web server (the 
frontend is based on React). It is available as `bci.gui` and exposes the 
following API:

```pycon
>>> from cortex.gui import run_server
>>> run_server(
...     host = '127.0.0.1',
...     port = 8080,
...     api_host = '127.0.0.1',
...     api_port = 5000,
... )
```

And the following CLI:

```sh
$ python -m cortex.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
```
The GUI consume the API and reflects it using a web server (the 
frontend is based on React). It is available as `bci.gui` and exposes the 
following API:

```pycon
>>> from cortex.gui import run_server
>>> run_server(
...     host = '127.0.0.1',
...     port = 8080,
...     api_host = '127.0.0.1',
...     api_port = 5000,
... )
```

And the following CLI:

```sh
$ python -m cortex.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
```