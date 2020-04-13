![build status](https://travis-ci.org/eitanhaimashiah/bci.svg?branch=master)
![coverage](https://codecov.io/gh/eitanhaimashiah/bci/branch/master/graph/badge.svg)

# BCI

Brain Computer Interface (BCI) is a system that can read minds, and upload 
snapshots of cognitions. Our system includes a [client](#the-client), which 
streams cognition snapshots to a [server](#the-server), which then publishes 
them to a [message queue](#the-message-queue-and-the-parses), where multiple 
[parsers](#the-message-queue-and-the-parses) read the snapshot, parse various 
parts of it, and publish the parsed results, which are then saved to a 
[database](#the-database-and-the-savers). The results are then exposed via a 
RESTful [API](#the-api), which is consumed by a [CLI](#the-cli); there's also 
a [GUI](#the-guiE
), which visualizes the results in various ways.

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

## Running the whole pipeline

1. To run the container of each component in the pipeline, execute: 

    ```sh
    $ ./scripts/run-pipeline.sh
    ...
    ```

2. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```
   
3. Once the above is done, you can do the following:
    * Invoke the [client](#the-client) to upload a sample to the server 
    running on http://localhost:8080.
    * 

    

## Usage

The `bci` package provides a command-line interface:

```sh
$ python -m bci --version
bci, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `run_server`, `upload_thought` and `run_webserver` commands:

```sh
$ python -m bci run_server "127.0.0.1:5000" data/
```
```sh
$ python -m bci upload_thought "127.0.0.1:5000" 1 "I'm sleepy"
done
```
```sh
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
```
Do note that each command's options should be passed to *that* command, so for 
example the `-q` and `-t` options should be passed to `bci`, not `run_server`, 
`upload_thought` or `run_webserver`.

```sh
$ python -m bci run_server -q "127.0.0.1:5000" data/ # this doesn't work
ERROR: no such option: -q
$ python -m bci -q run_server "127.0.0.1:5000" data/ # this does work
```

## The components

### The client
<!-- TODO Describe how a user can add a new driver -->

### The server

### The message queue and the parses
<!-- TODO Provide documentation about how to add a new parser: 
what would I need to do to be able to have the parse command invoke 
my own code, and the run-parser command to run it as a service 
working with a message queue. -->

### The database and the savers

### The API
 
### The CLI

### The GUI
